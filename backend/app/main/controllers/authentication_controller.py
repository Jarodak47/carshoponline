import uuid
from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __, get_language
# from app.main.core.mail import send_account_confirmation_email, send_reset_password_email, send_reset_password_option2_email
from app.main.core.mail import send_reset_password_email
from app.main.core.security import create_access_token, generate_code, get_password_hash, verify_password, \
    is_valid_password
from app.main.core.config import Config
from app.main.schemas.user import UserProfileResponse
from app.main.utils.helper import check_pass, generate_randon_key

router = APIRouter(prefix="/auths", tags=["auths"])


@router.post("/login", summary="Sign in with email and password", response_model=schemas.AdministratorAuthentication)
async def login(
        obj_in: schemas.Login,
        db: Session = Depends(get_db),
) -> schemas.AdministratorAuthentication:
    """
    Sign in with email and password
    """
    user = crud.user.authenticate(
        db, email=obj_in.email, password=obj_in.password
    )
    if not user:
        raise HTTPException(status_code=400, detail=__("auth-login-failed"))

    if user.status in [models.EnumList.BLOCKED, models.EnumList.DELETED, models.EnumList.UNACTIVED]:
        raise HTTPException(status_code=400, detail=__("auth-login-failed"))

    if not crud.user.is_active(user):
        raise HTTPException(status_code=402, detail=__("user-not-activated"))

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "user": user,
        "token": {
            "access_token": create_access_token(
                user.uuid, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        },
        "message":__("login-succes")
    }


@router.delete("/logout", response_model=schemas.Msg, status_code=200)
def logout(
        *,
        db: Session = Depends(get_db),
        request: Request,
        current_user: models.User = Depends(TokenRequired(roles=[])),
) -> Any:
    """
        Logout admininstrator session
    """

    user_token = (request.headers["authorization"]).split("Bearer")[1].strip()
    db.add(models.BlacklistToken(token=user_token, uuid=str(uuid.uuid4())))
    db.commit()

    return {"message": __("Ok")}


@router.get("/me", summary="Get current user", response_model=UserProfileResponse)
def get_current_user(
        current_user: models.User = Depends(TokenRequired()),
) -> schemas.UserProfileResponse:
    """
    Get current user
    """

    return current_user


@router.post("/password/token/send", summary="send token by mail for password reset when not logged in ", response_model=schemas.Msg)
def reset_password_step1(
        obj_in: schemas.ResetPasswordStep1,
        backgroundTasks: BackgroundTasks,
        db: Session = Depends(get_db)
) -> schemas.Msg:
    """
    Start reset password
    """
    user = crud.user.get_by_email(db=db, email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=__("user-not-activated"))

    # if not is_valid_password(password=obj_in.new_password):
    #     raise HTTPException(
    #         status_code=400,
    #         detail=__("password-invalid")
    #     )

    code = generate_randon_key(length=5)

    # user.otp_password = "00000"
    # user.otp_password_expired_at = datetime.now() + timedelta(minutes=5)

    user_code = models.UserActionValidation(
        uuid=str(uuid.uuid4()),
        code=str(code),
        user_uuid=user.uuid,
        value=code,
        expired_date=datetime.now() + timedelta(minutes=5)
    )
    db.add(user_code)
    db.commit()

    send_reset_password_email(
        backgroundTasks=backgroundTasks,
        email_to=user.email,
        prefered_language= get_language(),
        name=user.firstname,
        token=code, valid_minutes=5
    )

    return schemas.Msg(message=__("reset-password-started"))

@router.post("/password/token/validate",summary="verify token recived by mail for password request ", response_model=schemas.Msg)
def reset_password_step2(
        obj_in: schemas.ValidateAccount,
        db: Session = Depends(get_db),
) -> schemas.Msg:
    """
    validate password
    """

    user = crud.user.get_by_email(db, email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    user_code: models.UserActionValidation = db.query(models.UserActionValidation).filter(
        models.UserActionValidation.code == obj_in.token).filter(
        models.UserActionValidation.user_uuid == user.uuid).filter(
        models.UserActionValidation.expired_date >= datetime.now()).first()

    if not user_code:
        raise HTTPException(status_code=403, detail=__("invalid-user"))

    return {"message": __("Ok")}


@router.put("/password/new/", summary="Reset password step 2", response_model=schemas.Msg)
def reset_password_step3(
        obj_in: schemas.ResetPasswordStep2,
        db: Session = Depends(get_db),

) -> schemas.Msg:
    """
    Reset password step 3
    """
    user = crud.user.get_by_email(db, email=obj_in.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=__("user-email-not-found")
        )

    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=__("user-not-activated"))

    user_code: models.UserActionValidation = db.query(models.UserActionValidation).filter(
        models.UserActionValidation.code == obj_in.token).filter(
        models.UserActionValidation.user_uuid == user.uuid).filter(
        models.UserActionValidation.expired_date >= datetime.now()).first()

    if not user_code:
        raise HTTPException(
            status_code=404,
            detail=__("validation-code-not-found"),
        )

    if not is_valid_password(password=obj_in.new_password):
        raise HTTPException(
            status_code=400,
            detail=__("password-invalid")
        )

    db.delete(user_code)

    user.password_hash = get_password_hash(obj_in.new_password)
    db.add(user)
    db.commit()

    return schemas.Msg(message=__("password-reset-successfully"))


@router.put("/me/password/reset",summary="reset password when user is logged in ", response_model=schemas.UserProfileResponse)
async def reset_password(
        new_password: str,
        current_password: str,
        db: Session = Depends(get_db),
        # current_user: any = Depends(TokenRequired())
        current_user: models.User = Depends(TokenRequired())
) -> schemas.UserProfileResponse:
    """
        Update password of current connected user
    """
    if not verify_password(plain_password=current_password, hashed_password=current_user.password_hash):
        raise HTTPException(status_code=400, detail=__("incorrect-current-password"))

    # Check if new password is equal to current
    if verify_password(plain_password=new_password, hashed_password=current_user.password_hash):
        raise HTTPException(status_code=400, detail=__("different-password-required"))

    if not is_valid_password(password=new_password):
        raise HTTPException(status_code=400, detail=__("invalid-password"))

    current_user.password_hash = get_password_hash(new_password)

    db.commit()

    return current_user


@router.post("/account/token/send", summary="send token by mail for account validation ", response_model=schemas.Msg)
def send_token(
        obj_in: schemas.ResetPasswordStep1,
        backgroundTasks: BackgroundTasks,
        db: Session = Depends(get_db)
) -> schemas.Msg:
    """
    send
    """
    user = crud.user.get_by_email(db=db, email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    code = generate_randon_key(length=5)

    # user.otp_password = "00000"
    # user.otp_password_expired_at = datetime.now() + timedelta(minutes=5)

    user_code = models.UserActionValidation(
        uuid=str(uuid.uuid4()),
        code=str(code),
        user_uuid=user.uuid,
        value=code,
        expired_date=datetime.now() + timedelta(minutes=5)
    )
    db.add(user_code)
    db.commit()

    # send_reset_password_email(
    #     backgroundTasks=backgroundTasks,
    #     email_to=user.email,
    #     prefered_language= get_language(),
    #     name=user.firstname,
    #     token=code, valid_minutes=5
    # )



    return schemas.Msg(message=__("token-request-sent"))

@router.post("/account/validate",summary="Activate user account", response_model=schemas.UserAuthentication)
def validate_account(
        obj_in: schemas.ValidateAccount,
        db: Session = Depends(get_db),
) -> schemas.Msg:
    """
    validate Account
    """

    user = crud.user.get_by_email(db, email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    if user.otp != obj_in.token:
        raise HTTPException(status_code=400, detail=__("otp-invalid"))

    if user.otp_expired_at < datetime.now():
        raise HTTPException(status_code=400, detail=__("otp-expired"))

    user_code: models.UserActionValidation = db.query(models.UserActionValidation).filter(
        models.UserActionValidation.code == obj_in.token).filter(
        models.UserActionValidation.user_uuid == user.uuid).filter(
        models.UserActionValidation.expired_date >= datetime.now()).first()

    if not user_code:
        raise HTTPException(status_code=403, detail=__("invalid-code"))

    db.delete(user_code)
    db.commit()

    user.status = models.EnumList.ACTIVED
    # user.otp = None
    # user.otp_expired_at = None

    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "user": user,
        "token": {
            "access_token": create_access_token(
                user.uuid, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    }

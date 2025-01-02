from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create",summary = "create user by admin", response_model=schemas.AdministratorResponse, status_code=200)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AdministratorCreate,
    current_user:models.User = Depends(TokenRequired(roles =[]))
):
    """
    Create new user
    """
    
    admin = crud.user.get_by_email(db, obj_in.email)
    role = crud.role.get_by_uuid(db, obj_in.role_uuid)
    
    if not role:
        raise HTTPException(status_code=404, detail=__("role-not-found"))
    
    if obj_in.avatar_uuid:
        avatar = db.query(models.Storage).filter(models.Storage.uuid == obj_in.avatar_uuid).first()
        if not avatar:
            raise HTTPException(status_code=404, detail=__("avatar-not-found"))

    if admin and admin.role_uuid == obj_in.role_uuid:
        raise HTTPException(status_code=409, detail=__("user-email-taken"))
    
    return crud.user.create(db, obj_in,current_user)


@router.post("/register",summary = "register for customer", response_model=schemas.AdministratorResponse, status_code=200)
def register(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AdministratorCreate,
):
    """
    Create new user
    """
    
    admin = crud.user.get_by_email(db, obj_in.email)
    role = crud.role.get_by_uuid(db, obj_in.role_uuid)
    
    if not role:
        raise HTTPException(status_code=404, detail=__("role-not-found"))
    
    if obj_in.avatar_uuid:
        avatar = db.query(models.Storage).filter(models.Storage.uuid == obj_in.avatar_uuid).first()
        if not avatar:
            raise HTTPException(status_code=404, detail=__("avatar-not-found"))

    if admin and admin.role_uuid == obj_in.role_uuid:
        raise HTTPException(status_code=409, detail=__("user-email-taken"))
    
    return crud.user.create(db, obj_in)

# @router.post("/user/create",summary = "create user for customer or sim[le client", response_model=schemas.AdministratorResponse, status_code=200)
# def create(
#     *,
#     db: Session = Depends(get_db),
#     obj_in:schemas.AdministratorCreate,
#     current_user:models.User = Depends(TokenRequired(roles =[]))
# ):
#     """
#     Create new user
#     """
    
#     admin = crud.user.get_by_email(db, obj_in.email)
#     role = crud.role.get_by_uuid(db, obj_in.role_uuid)
    
#     if not role:
#         raise HTTPException(status_code=404, detail=__("role-not-found"))
    
#     if obj_in.avatar_uuid:
#         avatar = db.query(models.Storage).filter(models.Storage.uuid == obj_in.avatar_uuid).first()
#         if not avatar:
#             raise HTTPException(status_code=404, detail=__("avatar-not-found"))

#     if admin and admin.role_uuid == obj_in.role_uuid:
#         raise HTTPException(status_code=409, detail=__("user-email-taken"))
    
#     return crud.user.create(db, obj_in,current_user)

@router.put("", response_model=schemas.AdministratorResponse, status_code=201)
def update(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AdministratorUpdate,
    current_user:models.User = Depends(TokenRequired(roles =[] ))
):
    """
    Update new administrator
    """

    admin = crud.user.get_by_uuid(db, obj_in.uuid)
    if not admin:
        raise HTTPException(status_code=404, detail=__("user-not-found"))
    
    db_admin = crud.user.get_by_email(db, obj_in.email)

    if db_admin and admin.email != db_admin.email:
        raise HTTPException(status_code=409, detail=__("user-email-taken"))
    
    if obj_in.role_uuid:
        role = crud.role.get_by_uuid(db, obj_in.role_uuid)
        if not role:
            raise HTTPException(status_code=404, detail=__("role-not-found"))
    
    if obj_in.avatar_uuid:
        avatar = db.query(models.Storage).filter(models.Storage.uuid == obj_in.avatar_uuid).first()
        if not avatar:
            raise HTTPException(status_code=404, detail=__("avatar-not-found"))
        
    return crud.user.update(db, obj_in)

@router.delete("/{user_uuid}", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    user_uuid: str,
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
):
    """
    Delete administrator
    """
    admin = crud.user.get_by_uuid(db, user_uuid)
    if not admin:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    crud.user.soft_delete(db, user_uuid)
    return {"message": __("user-deleted")}

@router.get("/", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order:str = Query(None, enum =["ASC","DESC"]),
    user_uuid:Optional[str] = None,
    status: str = Query(None, enum =["ACTIVED","UNACTIVED"]),
    keyword:Optional[str] = None,
    # order_filed: Optional[str] = None
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.user.get_multi(
        db, 
        page, 
        per_page, 
        order,
        status,
        user_uuid,
        # order_filed
        keyword
    )
@router.get("/{user_uuid}", response_model=schemas.User)
def get(
    *,
    db: Session = Depends(get_db),
    user_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles =[] ))
):
    """
    get administrator with all data by passing filters
    """
    db_obj = crud.user.get_by_uuid(
        db, 
        user_uuid
    )
    
    if not db_obj:
        raise HTTPException(status_code=404, detail=__("user-not-found"))
    
    return db_obj
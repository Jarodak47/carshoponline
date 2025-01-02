from typing import Generator, Optional

from fastapi import Depends, Query
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from fastapi.encoders import jsonable_encoder
from app.main import models, crud, schemas
from app.main.core import security
from app.main.core.config import Config
from app.main.core.i18n import __
from app.main.core.security import decode_access_token
from app.main.models.db.session import SessionLocal


# def get_db(request: Request) -> Generator:
#     return request.state.db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuthUtils():

    @staticmethod
    def verify_jwt(token: str) -> bool:

        isTokenValid: bool = False

        try:
            payload = jwt.decode(
                token, Config.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = schemas.TokenPayload(**payload)
            return token_data
        except (jwt.InvalidTokenError, ValidationError) as e:
            print(e)
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid

    @staticmethod
    def verify_role(roles, user) -> bool:
        has_a_required_role = False
        if user.role_uuid:
            if isinstance(roles, str):
                if roles.lower() == user.role.code.lower():
                    has_a_required_role = True
            else:
                for role in roles:
                    if role.lower() == user.role.code.lower():
                        has_a_required_role = True
                        break
        return has_a_required_role



class TokenRequired(HTTPBearer):

    def __init__(self, token: Optional[str] = Query(None), roles=None, auto_error: bool = True):
        if roles is None:
            roles = []
        self.roles = roles
        self.token = token
        super(TokenRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        required_roles = self.roles
        credentials: HTTPAuthorizationCredentials = await super(TokenRequired, self).__call__(request)

        if not credentials and self.token:
            credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.token)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail=__("dependencies-token-invalid"))
            token_data = decode_access_token(credentials.credentials)
            if not token_data:
                print("+token-data+",token_data)
                raise HTTPException(status_code=403, detail=__("dependencies-token-invalid"))

            if models.BlacklistToken.check_blacklist(db, credentials.credentials):
                raise HTTPException(status_code=403, detail=__("dependencies-token-invalid"))

            current_user = crud.user.get_by_uuid(db=db, uuid=token_data["sub"])
            if not current_user:
                raise HTTPException(status_code=403, detail=__("dependencies-token-invalid"))

            if current_user.status != models.EnumList.ACTIVED:
                print("-------------",current_user)
                raise HTTPException(status_code=405, detail=__("user-not-active"))
            
            if required_roles:
                if not AuthUtils.verify_role(roles=required_roles, user=current_user):
                    raise HTTPException(status_code=403,
                                        detail=__("dependencies-access-unauthorized"))

            return current_user
        else:
            raise HTTPException(status_code=403, detail=__("dependencies-access-unauthorized"))
        db.close()

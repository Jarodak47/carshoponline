from datetime import datetime, date
from typing import List, Optional, Any
# from fastapi.params import Body
from fastapi import Body
from pydantic import BaseModel, ConfigDict, EmailStr

from app.main.schemas import DataList
from app.main.schemas.base import UserAuthentication
from app.main.schemas.file import File
from app.main.schemas.role import RoleBase


class Login(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordStep1(BaseModel):
    email: EmailStr
    language: str = "fr"


class ResetPasswordStep2(BaseModel):
    email: EmailStr
    token:str
    new_password: str


class ResetPasswordOption2Step1(BaseModel):
    email: EmailStr
    language: str = "fr"


class ResetPasswordOption2Step2(BaseModel):
    new_password: str
    token: str


class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    is_new_user: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class ValidateAccount(BaseModel):
    token: str
    email:EmailStr

class User(UserBase):
    phonenumber: Optional[str] = None
    address: Optional[str] = None
    uuid: Optional[str] = None
    role:RoleBase
    date_added: datetime
    date_modified: datetime


class Storage(BaseModel):
    uuid: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None
    mimetype: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size: Optional[int] = None
    thumbnail: Any = None
    medium: Any = None
    date_added: Optional[datetime] = None
    date_modified: Optional[datetime] = None

class UserSlim(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: str
    lastname: str
    is_new_user: Optional[bool] = False
    # role:RoleBase
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(UserBase):
    uuid: Optional[str] = None
    role: RoleBase
    ok:bool = True
    clientToken: str ="Ok"  # Ajoutez le token client ici
    date_added: datetime
    date_modified: datetime
    avatar: Optional[Storage] = None

class UserMe(BaseModel):
    user:UserProfileResponse



class UserDetail(User):
    uuid: str
    avatar: Optional[Storage] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserList(DataList):
    data: List[User] = []


class UserUpdate(BaseModel):
    user_uuid: str
    country_code: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    storage_uuid: str = None


# class Avatar(BaseModel):
#     uuid:str
#     file_name:str
#     url:str
#     mimetype:str
#     width:int
#     height:int
#     size:int
#     thumbnail:Any
#     medium:Any
#     date_added:Any
#     date_modified:Any

class Roleslim(BaseModel):
    uuid:str
    title_fr:str
    title_en: str
    code:str

    model_config = ConfigDict(from_attributes=True)


class AdministratorBase(BaseModel):
    email:EmailStr
    firstname: str
    lastname: str
    role_uuid:str

class AdministratorCreate(AdministratorBase):
    avatar_uuid:Optional[str] = None
    password:str
    phonenumber:str
    address:str

class AdministratorUpdate(AdministratorBase):
    uuid:str
    email:Optional[EmailStr]=None
    firstname: Optional[str]=None
    lastname: Optional[str]=None
    role_uuid: Optional[str]=None
    avatar_uuid: Optional[str]=None
    phonenumber: Optional[str]=None
    address: Optional[str]=None


class AdministratorDelete(BaseModel):
    uuid:str

class AdministratorResponse(AdministratorBase):
    uuid:str
    status:str
    phonenumber:Optional[str] = None
    address:str = Body(...)
    avatar : Optional[File]
    role: Roleslim
    date_added: Any
    date_modified: Any

    model_config = ConfigDict(from_attributes=True)

class AdministratorResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[AdministratorResponse]

    model_config = ConfigDict(from_attributes=True)


class Administrator(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: str
    lastname: str
    is_new_user: Optional[bool] = False
    avatar: Optional[File]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)

# class User(BaseModel):
#     uuid: Optional[str] = None
#     email: EmailStr
#     firstname: str
#     lastname: str
#     role:Roleslim
#     is_new_user: Optional[bool] = False
#     avatar: Optional[File]
#     date_added: datetime
#     date_modified: datetime

#     model_config = ConfigDict(from_attributes=True)

class AdministratorAuthentication(UserAuthentication):
    user: User

    model_config = ConfigDict(from_attributes=True)
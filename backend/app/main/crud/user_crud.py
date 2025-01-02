from datetime import datetime, timedelta
import math
from typing import Union, Optional, List
from pydantic import EmailStr
from sqlalchemy import or_
from app.main.core.i18n import __
# from app.main.core.mail import send_account_creation_email, send_reset_password_email
from app.main.crud.base import CRUDBase
from sqlalchemy.orm import Session,joinedload
from app.main import schemas, models
import uuid
from app.main.core.security import get_password_hash, verify_password, generate_password


class CRUDUser(CRUDBase[models.User, schemas.AdministratorCreate,schemas.AdministratorUpdate]):

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str) -> Union[models.User, None]:
        user = db.query(models.User).\
            filter(models.User.uuid == uuid,
                   models.User.status==models.EnumList.ACTIVED
                ).first()
        
        print("user12345",user)
        return user
    
    @classmethod
    def create(cls, db: Session, obj_in: schemas.AdministratorCreate,current_user:Optional[models.User]= None) -> models.User:
        # password:str = generate_password(8, 8)
        # send_account_creation_email(email_to=obj_in.email,prefered_language="en", name=obj_in.firstname,password=password)
        administrator = models.User(
            uuid= str(uuid.uuid4()),
            firstname = obj_in.firstname,
            lastname = obj_in.lastname,
            address = obj_in.address,
            phonenumber = obj_in.phonenumber,
            email = obj_in.email,
            password_hash = get_password_hash(obj_in.password),
            role_uuid = obj_in.role_uuid if obj_in.role_uuid else None,
            avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else None,
            added_by_uuid = current_user.uuid if current_user else None,
            status = models.EnumList.ACTIVED
        )
        db.add(administrator)
        db.commit()
        db.refresh(administrator)
    
        return administrator
    
    @classmethod
    def update(cls, db: Session,obj_in: schemas.AdministratorUpdate) -> models.User:
        administrator = cls.get_by_uuid(db, obj_in.uuid)
        administrator.firstname = obj_in.firstname if obj_in.firstname else administrator.firstname
        administrator.lastname = obj_in.lastname if obj_in.lastname else administrator.lastname
        administrator.email = obj_in.email if obj_in.email else administrator.email
        administrator.role_uuid = obj_in.role_uuid if obj_in.role_uuid else administrator.role_uuid
        administrator.avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else administrator.avatar_uuid
        administrator.address = obj_in.address if obj_in.address else administrator.address
        administrator.phonenumber = obj_in.phonenumber if obj_in.phonenumber else administrator.phonenumber

        db.commit()
        db.refresh(administrator)
        return administrator
    
    @classmethod
    def delete(cls,db:Session, uuid) -> models.User:
        administrator = cls.get_by_uuid(db, uuid)
        db.delete(administrator)
        db.commit()
    
    @classmethod
    def soft_delete(cls,db:Session, uuid) -> models.User:
        administrator = cls.get_by_uuid(db, uuid)
        administrator.status = models.EnumList.DELETED
        db.commit()
    
    @classmethod
    def get_by_email(cls,db:Session,email:EmailStr) -> models.User:
        return db.query(models.User).filter(models.User.email == email).first()
    
    @classmethod
    def get_multi(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 30,
        order:Optional[str] = None,
        status:Optional[str] = None,
        user_uuid:Optional[str] = None,
        keyword:Optional[str]= None
        # order_filed:Optional[str] = None   
    ):
        record_query = db.query(models.User).options(joinedload(models.User.role))

        # if order_filed:
        #     record_query = record_query.order_by(getattr(models.Administrator, order_filed))

        record_query = record_query.filter(models.User.status.not_in(["DELETED","BLOCKED"]))
        
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.User.firstname.ilike('%' + str(keyword) + '%'),
                    models.User.email.ilike('%' + str(keyword) + '%'),
                    models.User.lastname.ilike('%' + str(keyword) + '%'),
                    # models.Role.title_fr.ilike('%' + str(keyword) + '%'),
                    # models.Role.title_en.ilike('%' + str(keyword) + '%'),

                )
            )
        if status:
            record_query = record_query.filter(models.User.status == status)
        
        if order and order.lower() == "asc":
            record_query = record_query.order_by(models.User.date_added.asc())
        
        elif order and order.lower() == "desc":
            record_query = record_query.order_by(models.User.date_added.desc())

        if user_uuid:
            record_query = record_query.filter(models.User.uuid == user_uuid)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.AdministratorResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )


    @classmethod
    def authenticate(cls, db: Session, email: str, password: str) -> Optional[models.User]:
        db_obj: models.User = db.query(models.User).filter(
            models.User.email == email,
        ).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None
        return db_obj


    def is_active(self, user: models.User) -> bool:
        return user.status == models.EnumList.ACTIVED
    
user = CRUDUser(models.User)



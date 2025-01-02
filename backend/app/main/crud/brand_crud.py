from typing import Union, Optional
# from app.main.core.mail import send_account_creation_email, send_reset_password_email
from app.main.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.main import schemas, models
import uuid


class CRUDBrand(CRUDBase[models.Brand, schemas.BrandCreate,schemas.BrandUpdate]):


    def get_by_uuid(cls,db: Session, uuid: str) -> Union[models.Brand, None]:
        return db.query(models.Brand).filter(models.Brand.uuid == uuid).first()
    
    def get_by_slug(cls,db: Session, slug: str) -> Union[models.Brand, None]:
        return db.query(models.Brand).filter(models.Brand.slug == slug).first()
    
    
    @classmethod
    def create(cls, db: Session, obj_in: schemas.BrandCreate) -> models.Brand:
        
        brand = models.Brand(
            uuid= str(uuid.uuid4()),
            name = obj_in.name,
            slug = cls.slugify(cls,obj_in.name),
            logo_uuid = obj_in.logo_uuid
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)
    
        return brand
    
    @classmethod
    def update(cls, db: Session,brand_uuid,name) -> models.Brand:
        brand = cls.get_by_uuid(cls,db, brand_uuid)
        
        # brand.logo_uuid = obj_in.logo_uuid if obj_in.logo_uuid else brand.logo_uuid
        brand.name = name if name else brand.name
        brand.slug = cls.slugify(cls,name)

        db.commit()
        db.refresh(brand)
        return brand
    
    @classmethod
    def delete(cls,db:Session, uuids:list[str]):
        for uuid in uuids:
            super().remove(db,uuid=uuid)
    
    def soft_delete(cls,db:Session, uuids:list[str]):
        for uuid in uuids:
            super().soft_delete(db,uuid=uuid)
    
    def get_multi(
        self,
        db:Session,
        page:int = 1,
        per_page:int = 30,
        *,
        obj_in:Optional[schemas.BrandSearchRequest]
    ):
        return super().get_multi(
            db,
            page = page,
            per_page = per_page,
            filters=obj_in
        )

brand = CRUDBrand(models.Brand)



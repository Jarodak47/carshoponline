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


class CRUDAd(CRUDBase[models.Ad, schemas.AdCreate,schemas.AdUpdate]):

    def get_by_uuid(cls, db: Session, uuid: str) -> Union[models.Ad, None]:
        return super().get(db, uuid)
    
    @classmethod
    def create(cls, db: Session, obj_in: schemas.AdCreate) -> models.Ad:
        
        vehicle = models.Ad(
            uuid= str(uuid.uuid4()),
            brand = obj_in.brand,
            model = obj_in.model,
            year = obj_in.year,
            color = obj_in.color,
            quantity = obj_in.quantity,
            is_rentable = obj_in.is_rentable,
            is_purchasable = obj_in.is_purchasable,
            is_bookable = obj_in.is_bookable,
            status = models.EnumList.AVAILABLE
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
    
        return vehicle
    
    def create1(self,db: Session, obj_in: schemas.AdCreate) -> models.Ad:
        
        obj_in_data = obj_in.dict()
        # obj_in_data = obj_in.model_dump(exclude_unset=True
        obj_in_data["uuid"] = str(uuid.uuid4())
        valid_fields = {key: value for key, value in obj_in_data.items() if hasattr(models.Ad, key)}

        db_obj = super().create(db,valid_fields)

        new_add_vehicle =  models.AdVehicle(
            uuid = str(uuid.uuid4()),
            ad_uuid = db_obj.uuid,
            vehicle_uuid = obj_in.vehicle_uuid,
        )
        db.add(new_add_vehicle)

        for photo_uuid in obj_in.photo_uuids:
            new_ad_photo = models.AdPhoto(
                # uuid = str(uuid.uuid4()),
                ad_vehicle_uuid = new_add_vehicle.uuid,
                photo_uuid = photo_uuid
            )
            db.add(new_ad_photo)
            
        db.commit()
        return db_obj

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
        obj_in:Optional[schemas.AdSearchRequest]
    ):
        return super().get_multi(
            db,
            page = page,
            per_page = per_page,
            filters=obj_in
        )

ad = CRUDAd(models.Ad)



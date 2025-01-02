from typing import Union, Optional
# from app.main.core.mail import send_account_creation_email, send_reset_password_email
from app.main.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.main import schemas, models
import uuid


class CRUDVehicle(CRUDBase[models.Vehicle, schemas.VehicleCreate,schemas.VehicleUpdate]):

    def get_by_uuid(cls, db: Session, uuid: str) -> Union[models.Vehicle, None]:
        return super().get(db, uuid)
    
    def get_by_uuid_and_brand_uuid(cls, db: Session, vehicle_uuid: str, brand_uuid: str) -> Union[schemas.RelatedVehicleForBrand, None]:
        return db.query(models.Vehicle).filter(models.Vehicle.uuid == vehicle_uuid,models.Vehicle.brand_uuid == brand_uuid).first()
    
    def get_by_slug(cls,db: Session, slug: str) -> Union[models.Vehicle, None]:
        return db.query(models.Vehicle).filter(models.Vehicle.slug == slug).first()
    
    @classmethod
    def create(cls, db: Session, obj_in: schemas.VehicleCreate) -> models.Vehicle:
        
        vehicle = models.Vehicle(
            uuid= str(uuid.uuid4()),
            brand_uuid = obj_in.brand_uuid,
            model = obj_in.model,
            slug = cls.slugify(cls,obj_in.model),
            year = obj_in.year,
            color = obj_in.color,
            quantity = obj_in.quantity,
            is_rentable = obj_in.is_rentable,
            is_purchasable = obj_in.is_purchasable,
            is_bookable = obj_in.is_bookable,
            status = models.EnumList.AVAILABLE,
            description = obj_in.description,
            price = obj_in.price,
            fuelType = obj_in.fuelType,
            transmission = obj_in.transmission,
            engineSize = obj_in.engineSize,
            mileage = obj_in.mileage,
            safetyrating = obj_in.safetyrating,
            warranty = obj_in.warranty,
            seater = obj_in.seater,
            size = obj_in.size,
            fuelTank = obj_in.fuelTank
        )
        db.add(vehicle)

        for image_uuid in obj_in.image_uuids:
            vehicle_image = models.VehicleImage(
                uuid= str(uuid.uuid4()),
                vehicle_uuid = vehicle.uuid,
                image_uuid = image_uuid
            )
            db.add(vehicle_image)

        db.commit()
        db.refresh(vehicle)
    
        return vehicle
    
    def create1(self,db: Session, obj_in: schemas.VehicleCreate) -> models.Vehicle:
        
        obj_in_data = obj_in.dict()
        obj_in_data["uuid"] = str(uuid.uuid4())
        obj_in_data["status"] = models.EnumList.AVAILABLE
        return super().create(db,obj_in_data)
    
    @classmethod
    def update(cls, db: Session,obj_in: schemas.VehicleUpdate) -> models.Vehicle:
        vehicle = cls.get_by_uuid(db, obj_in.uuid)
        
        vehicle.model = obj_in.model if obj_in.model else vehicle.model
        vehicle.color = obj_in.color if obj_in.color else vehicle.color
        vehicle.description = obj_in.description if obj_in.description else vehicle.description

        vehicle.is_rentable = obj_in.is_rentable if obj_in.is_rentable else vehicle.is_rentable
        vehicle.is_purchasable = obj_in.is_purchasable if obj_in.is_purchasable else vehicle.is_purchasable
        vehicle.is_bookable = obj_in.is_bookable if obj_in.is_bookable else vehicle.is_bookable

        vehicle.quantity = obj_in.quantity if obj_in.quantity else vehicle.quantity
        vehicle.year = obj_in.year if obj_in.year else vehicle.year

        db.commit()
        db.refresh(vehicle)
        return vehicle
    
    def update1(cls, db: Session,obj_in: schemas.VehicleUpdate,db_obj:models.Vehicle) -> models.Vehicle:
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        obj_in_data['slug'] = cls.slugify(obj_in_data['model'])
        return super().update(db,db_obj,obj_in_data)
    
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
        obj_in:Optional[schemas.VehicleSearchRequest]
    ):
        return super().get_multi(
            db,
            page = page,
            per_page = per_page,
            filters=obj_in
        )

vehicle = CRUDVehicle(models.Vehicle)



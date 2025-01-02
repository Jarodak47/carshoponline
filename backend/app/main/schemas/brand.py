from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional,Any
from .import DataList
from datetime import datetime

class VehicleInBrand(BaseModel):
    uuid:str
    model: str
    slug: str
    year: int
    color: str
    is_rentable: bool = False
    is_purchasable: bool = False
    is_bookable: bool = False
    quantity: int = 1
    description: Optional[str] = None
    price: float
    fuelType: str
    transmission: str
    engineSize: float
    mileage: int
    safetyrating: int
    warranty: Optional[str] = None
    seater: int
    size: str
    fuelTank: float
    productPictures:list[str]
    model_config = ConfigDict(from_attributes=True)

class BrandBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class BrandCreate(BrandBase):
    logo_uuid: str

class BrandUpdate(BrandBase):
    uuid: str
    name:Optional[str] = None
    logo_uuid:Optional[str] = None


class Brand(BrandBase):
    uuid: str
    slug: str
    success:bool = True
    brandPictures:str
    publicPicture_id:str
    vehicles: list[VehicleInBrand]
    vehicle_count:int
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)

class BrandSearchRequest(BrandBase):
    status:Optional[str] = None
    order: Optional[str] = None
    order_filed: Optional[str] = 'date_added'
    
    @model_validator(mode='before')
    def set_optional(cls, values):
        return {
            k: (v or None) for k, v in values.items()
        }
    
    model_config = ConfigDict(
        from_attributes=True,
    )

    
class BrandResponseList(DataList):
    data:list[Brand] =[]
    success:bool = True




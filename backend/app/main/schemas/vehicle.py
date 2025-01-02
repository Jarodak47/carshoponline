from typing import Optional
from pydantic import BaseModel, ConfigDict,model_validator,field_validator
from . import DataList,DateDisplayBase
from .brand import Brand


class VehicleBase(BaseModel):
    model: str
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

class VehicleCreate(VehicleBase):
    brand_uuid: str
    image_uuids:list[str]

class VehicleUpdate(VehicleBase):
    uuid : str
    brand_uuid: Optional[str] = None
    image_uuids:list[str] =[]
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    is_rentable: bool = False
    is_purchasable: bool = False
    is_bookable: bool = False
    quantity: Optional[int] = 1
    description: Optional[str] = None
    price: Optional[float] = None
    fuelType: Optional[str] = None
    transmission: Optional[str] = None
    engineSize: Optional[float] = None
    mileage: Optional[int] = None
    safetyrating: Optional[int] = None
    warranty: Optional[str] = None
    seater: Optional[int] = None
    size: Optional[str] = None
    fuelTank: Optional[float] = None

    @model_validator(mode='before')
    @classmethod
    def set_optional(cls, values):
        if isinstance(values, dict):
            for k, v in values.items():
                if not isinstance(v, bool) and k != 'uuid':
                    values[k] = v or None
        return values
    
    model_config = ConfigDict(from_attributes=True)

       

class Vehicle(VehicleBase,DateDisplayBase):
    uuid:str
    slug: str
    status:str
    brand:Brand
    productPictures:list[str]
    publicPicture_ids:list[str]
    model_config = ConfigDict(from_attributes=True)

class VehicleSlim(VehicleBase):
    slug: str
    uuid:str
    model_config = ConfigDict(from_attributes=True)

    
class VehicleSearchRequest(VehicleBase):
    slug: str
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
        exclude={'is_rentable','is_purchasable','is_bookable','quantity'}
    )

    
class VehicleResponseList(DataList):
    data:list[Vehicle] =[]

class RelatedVehicleForBrand(BaseModel):
    total_count:int
    success:bool = True
    message:str = "Related Vehicles for this brand"
    vehicles:list[Vehicle]
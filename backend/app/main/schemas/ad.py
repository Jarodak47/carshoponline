from datetime import datetime
from typing import Optional,Any
from pydantic import BaseModel, ConfigDict,model_validator
# from pydantic.class_validators import validator
from . import DataList,File,DateDisplayBase,VehicleSlim
from fastapi import Body


class AdBase(BaseModel):
    title: str
    description: str = Body(...)


class AdCreate(AdBase):
    vehicle_uuid: str
    photo_uuids:list[str]

class AdUpdate(AdBase):
    uuid: str
    photo_uuids:list[str]
    @model_validator(mode='before')
    def set_optional(cls, values):
        for k,v in values.items():
            if isinstance(v,bool):
                pass
            elif k!='uuid':
                values[k] = v or None
            
        return values

class AdPhoto(BaseModel):
    ad_vehicle_uuid:str 
    photo:File
    model_config = ConfigDict(from_attributes=True)

    
class AdVehicle(BaseModel):
    uuid: str
    ad_uuid:str
    vehicle:VehicleSlim
    photos:list[AdPhoto]
    model_config = ConfigDict(from_attributes=True)


class Ad(AdBase,DateDisplayBase):
    uuid: str
    vehicles:list[AdVehicle]
    model_config = ConfigDict(from_attributes=True)

class AdSearchRequest(AdBase):
    order: Optional[str] = None
    order_filed: Optional[str] = 'date_added'
    
    @model_validator(mode='before')
    def set_optional(cls, values):
        return {
            k: (v or None) for k, v in values.items()
        }

class AdResponseList(DataList):
    data:list[Ad] =[]

    


       


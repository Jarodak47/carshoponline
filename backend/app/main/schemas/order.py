from typing import  Any
# from fastapi.params import Body
from pydantic import BaseModel, ConfigDict

from app.main.schemas.base import DateDisplayBase
from app.main.schemas.user import UserSlim




class OrderResponse(DateDisplayBase,BaseModel):
    uuid:str
    quantity:int
    total_amount:float
    status:str
    payment:dict[str,Any]
    products:Any
    buyer:UserSlim
    model_config = ConfigDict(from_attributes=True)


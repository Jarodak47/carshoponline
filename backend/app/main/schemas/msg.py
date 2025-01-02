from pydantic import BaseModel
from typing import Optional, Text


class Msg(BaseModel):
    message: str

class TextMessage(BaseModel):
    contain: Optional[Text]


class BoolStatus(BaseModel):
    status: bool


class DataDisplay(BaseModel):
    data: str

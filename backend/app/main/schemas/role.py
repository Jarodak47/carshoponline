from datetime import datetime, date
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict



class RoleBase(BaseModel):
    title_fr: str
    title_en: str
    code: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    uuid:str
    title_fr: Optional[str] = None
    title_en: Optional[str] = None
    code :Optional[str] = None
    description: Optional[str] = None

class RoleInDB(RoleBase):
    uuid: str
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)

class Role(RoleInDB):
    pass


class RoleSchema(BaseModel):
    uuid: str
    title_fr: str
    title_en: str
    code: str
    description: Optional[str] = None

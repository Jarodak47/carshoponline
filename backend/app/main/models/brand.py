from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event,Float
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.main.models.user import EnumList
from .db.base_class import Base
from .base import TimesTampMixin

@dataclass
class Brand(Base,TimesTampMixin):
    __tablename__ = 'brands'

    uuid: str = Column(String, primary_key=True, index=True)
    name: str = Column(String, nullable=False, index=True,unique=True)
    slug: str = Column(String, nullable=False, index=True,unique=True)

    status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.NONE)

    logo_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=False)
    logo = relationship('Storage')

    vehicles = relationship('Vehicle', back_populates='brand', cascade="all, delete-orphan")
    
    @hybrid_property
    def brandPictures(self):
        return self.logo.url if self.logo else ""
    
    @hybrid_property
    def publicPicture_id(self):
        return self.logo.public_id if self.logo else ""
    
    @hybrid_property
    def vehicle_count(self):
        return len([i for i in self.vehicles if self.vehicles and i.status!="DELETED"]) 

    



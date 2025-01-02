from dataclasses import dataclass

from .base import TimesTampMixin   
from sqlalchemy import Column,String, DateTime, Text,event
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base




@dataclass
class Role(TimesTampMixin,Base):
    """
    Database model for storing Role related details
    """
    __tablename__ = 'roles'

    uuid: str = Column(String, primary_key=True, unique=True,index = True)
    code: str = Column(String, unique=True,index = True)
    title_fr: str = Column(String(100), unique=True, index=True)
    title_en: str = Column(String(100), unique=True, index=True)
    description: str = Column(Text)


    def __repr__(self):
        return '<Role: uuid: {} title_fr: {} title_en: {} code: {} group: {}>'.format(self.uuid, self.title_fr, self.title_en,self.code,self.group)
    

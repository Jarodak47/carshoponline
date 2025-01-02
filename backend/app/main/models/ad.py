from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event,Float
from datetime import datetime
from sqlalchemy.orm import relationship
from .db.base_class import Base
from .import TimesTampMixin,EnumList

@dataclass
class Ad(TimesTampMixin,Base):
    __tablename__ = 'ads'

    uuid: str = Column(String, primary_key=True, unique=True)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.NONE)

    vehicles = relationship('AdVehicle', back_populates='ad')
    notification = relationship('Notification', back_populates='ad', uselist=False)
    ad_reviews = relationship('AdReview', back_populates='ad')

@dataclass
class AdVehicle(TimesTampMixin,Base):
    __tablename__ = 'ad_vehicles'
    uuid: str = Column(String, primary_key=True, unique=True)
    ad_uuid: str = Column(String, ForeignKey('ads.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    vehicle_uuid: str = Column(String, ForeignKey('vehicles.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    
    photos = relationship('AdPhoto', back_populates='ad_vehicle')
    ad = relationship('Ad', back_populates='vehicles')
    vehicle = relationship('Vehicle', back_populates='ads')

@dataclass
class AdPhoto(TimesTampMixin,Base):
    __tablename__ = 'ad_photos'
    # uuid: str = Column(String, primary_key=True, unique=True)
    ad_vehicle_uuid: str = Column(String, ForeignKey('ad_vehicles.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    photo_uuid: str = Column(String, ForeignKey('storages.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)

    ad_vehicle = relationship('AdVehicle', back_populates='photos')
    photo = relationship('Storage')

@dataclass
class AdReview(TimesTampMixin,Base):
    __tablename__ = 'ad_reviews'

    user_uuid: str = Column(String, ForeignKey('users.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    ad_uuid: str = Column(String, ForeignKey('ads.uuid',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    rating: float = Column(Float, nullable=False)
    comment: str = Column(Text, nullable=True)
   
    user = relationship('User', back_populates='ad_reviews')
    ad = relationship('Ad', back_populates='ad_reviews')

from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean,types,Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.main.models.user import EnumList
from .db.base_class import Base
from .base import TimesTampMixin

@dataclass
class Vehicle(TimesTampMixin,Base):
    __tablename__ = 'vehicles'

    uuid: str = Column(String, primary_key=True, index=True)
    brand_uuid: str = Column(String, ForeignKey('brands.uuid'), nullable=False)
    brand = relationship('Brand', back_populates='vehicles')
    model: str = Column(String, nullable=False, index=True)
    
    slug: str = Column(String, nullable=True, index=True,unique=True)

    year: int = Column(Integer, nullable=False, index=True)
    color: str = Column(String, nullable=False, index=True)
    description: str = Column(String, nullable=True)
    quantity: int = Column(Integer, nullable=False, index=True)

    is_rentable: bool = Column(Boolean, nullable=False, default=False)
    is_purchasable: bool = Column(Boolean, nullable=False, default=False)
    is_bookable: bool = Column(Boolean, nullable=False, default=False)

    price: float = Column(Float, nullable=False)
    fuelType: str = Column(String, nullable=False)
    transmission: str = Column(String, nullable=False)

    engineSize: float = Column(Float, nullable=False)
    mileage: int = Column(Integer, nullable=False)
    safetyrating: int = Column(Integer, nullable=False)

    warranty: str = Column(String, nullable=True)
    seater: int = Column(Integer, nullable=False)
    size: str = Column(String, nullable=False)
    
    fuelTank: float = Column(Float, nullable=False)
    brand = relationship('Brand', back_populates='vehicles')
    status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.UNACTIVED)

    ads = relationship('AdVehicle', back_populates='vehicle')
    
    images = relationship('VehicleImage', back_populates='vehicle', cascade="all, delete-orphan")


    def __repr__(self):
        return f'<Vehicle: brand: {self.brand}, model: {self.model}, year: {self.year}, color: {self.color}, is_rentable: {self.is_rentable}, is_purchasable: {self.is_purchasable}>'
    
    @hybrid_property
    def productPictures(self):
        return [i.image.url for i in self.images if self.images]
    
    @hybrid_property
    def publicPicture_ids(self):
        return [i.image.public_id for i in self.images if self.images]

@dataclass
class VehicleImage(Base,TimesTampMixin):
    __tablename__ = 'vehicle_images'

    uuid: str = Column(String, primary_key=True, index=True)
    vehicle_uuid: str = Column(String, ForeignKey('vehicles.uuid'), nullable=False)
    vehicle = relationship('Vehicle', back_populates='images')
    # status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.NONE)
    
    image_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=False)
    image = relationship('Storage')

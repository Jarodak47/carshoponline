from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, String, Integer,types,Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB


from .user import EnumList
from .db.base_class import Base
from .base import TimesTampMixin


@dataclass
class Payment(TimesTampMixin,Base):
    __tablename__ = 'payments'

    uuid: str = Column(String, primary_key=True, index=True,unique=True)
    order_uuid: str = Column(String, ForeignKey("orders.uuid"), nullable=False,primary_key=True)

    status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.PROCESSED)

    total_paid: float = Column(Float, nullable=False)
    total_due: float = Column(Float, nullable=False,default=0.0)
    type: str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.NONE)


@dataclass
class Order(Base,TimesTampMixin):
    __tablename__ = "orders"

    uuid: str = Column(String, primary_key=True, index=True)
    buyer_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)
    quantity: int = Column(Integer, nullable=False, index=True)
    payment: any = Column(JSONB, default={}, nullable=True)
    products: any = Column(JSONB, default={}, nullable=True)

    total_amount: float = Column(Float, nullable=False)
    status:str = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.NOT_PROCESSED)

    buyer = relationship("User", backref="orders")
    


@dataclass
class OrderVehicle(Base):
    __tablename__ = "order_vehicles"

    order_uuid: str = Column(String, ForeignKey("orders.uuid"), primary_key=True)
    vehicle_uuid: str = Column(String, ForeignKey("vehicles.uuid"),primary_key=True)
    order = relationship("Order", backref="vehicles")
    vehicle = relationship("Vehicle", backref="orders")

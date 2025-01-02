from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, ForeignKey, String,DateTime,event,types
from datetime import datetime
from sqlalchemy.orm import relationship

from .base import TimesTampMixin,EnumList
from .db.base_class import Base

# class Reservation(Base):
#     __tablename__ = 'reservations'

#     user_uuid: str = Column(String, ForeignKey('users.uuid'), primary_key=True)
#     vehicle_uuid: str = Column(String, ForeignKey('vehicles.uuid'), primary_key=True)

#     period_from: datetime = Column(DateTime, nullable=False)
#     period_to: datetime = Column(DateTime, nullable=False)
#     pph: float = Column(Float, nullable=False)

#     user = relationship('User', back_populates='reservations')
#     vehicle = relationship('Vehicle', back_populates='reservations')
#     date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())
#     date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

@dataclass
class User(TimesTampMixin,Base):
    """
    User model for storing users related details
    """
    __tablename__ = 'users'

    uuid: str = Column(String, primary_key=True, unique=True)

    email: str = Column(String, nullable=False, default="", index=True)
    firstname: str = Column(String(100), nullable=False, default="")
    lastname: str = Column(String(100), nullable=False, default="")

    avatar_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid])

    role_uuid: str = Column(String, ForeignKey('roles.uuid'), nullable=False)
    role = relationship("Role", foreign_keys=[role_uuid],uselist = False)

    password_hash: str = Column(String(100), nullable=True, default="")
    status = Column(types.Enum(EnumList), index=True, nullable=False, default=EnumList.UNACTIVED)
    
    phonenumber = Column(String, index=True, nullable=False)
    address = Column(String, index=True, nullable=False)

    otp: str = Column(String(5), nullable=True, default="")
    otp_expired_at: datetime = Column(DateTime, nullable=True, default=None)

    otp_password: str = Column(String(5), nullable=True, default="")
    otp_password_expired_at: datetime = Column(DateTime, nullable=True, default=None)
    
    added_by_uuid: str = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)

    # reservations = relationship('Reservation', back_populates='user')
    ad_reviews = relationship('AdReview', back_populates='user')
    notifications = relationship('UserNotification', back_populates='user')

    def __repr__(self):
        return '<User: uuid: {} email: {}>'.format(self.uuid, self.email)


class UserActionValidation(TimesTampMixin,Base):
    __tablename__ = 'user_action_validations'

    uuid: str = Column(String, primary_key=True)

    user_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    code: str = Column(String, unique=False, nullable=True)
    expired_date: any = Column(DateTime, default=datetime.now())
    value: str = Column(String, default="", nullable=True)




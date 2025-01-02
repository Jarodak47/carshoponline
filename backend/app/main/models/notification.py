from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, ForeignKey, String,DateTime,event,types
from datetime import datetime
from sqlalchemy.orm import relationship

from .base import TimesTampMixin
from .db.base_class import Base

class Notification(TimesTampMixin,Base):
    __tablename__ = 'notifications'

    uuid: str = Column(String, primary_key=True, index=True)
    ad_uuid: str = Column(String, ForeignKey('ads.uuid'), unique=True, nullable=False)

    message: str = Column(String, nullable=False)
    

    ad = relationship('Ad', back_populates='notification')
    users = relationship('UserNotification', back_populates='notification')

class UserNotification(Base):
    __tablename__ = 'user_notifications'

    user_uuid: str = Column(String, ForeignKey('users.uuid'), primary_key=True)
    notification_uuid: int = Column(String, ForeignKey('notifications.uuid'), primary_key=True)

    user = relationship('User', back_populates='notifications')
    user = relationship('User', foreign_keys=[user_uuid])
    notification = relationship('Notification', back_populates='users')
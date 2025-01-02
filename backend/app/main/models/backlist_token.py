from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, String, event

from app.main.models.db.base_class import Base
from .base import TimesTampMixin

@dataclass
class BlacklistToken(TimesTampMixin,Base):
    __tablename__ = 'blacklist_tokens'

    uuid = Column(String, primary_key=True, unique=True)
    token = Column(String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<BlacklistToken: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(db, auth_token):
        # check whether auth token has been blacklisted
        res = db.query(BlacklistToken).filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


from enum import Enum
from sqlalchemy import Column,DateTime,event
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

class EnumList(str, Enum):
    ACTIVED = "ACTIVED"
    UNACTIVED = "UNACTIVED"
    DELETED = "DELETED"
    BLOCKED = "BLOCKED"
    
    RENTAL = "RENTAL" #location
    PURCHASE = "PURCHASE" #achat

    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    CANCEL = "CANCEL"
    DELIVERED ="DELIVERED"
    NOT_PROCESSED ="NOT_PROCESSED"
    PROCESSED = "PROCESSED"

    SALE = "SALE" #vente
    BOOKING = "BOOKING" #reservation
    NONE = "NONE" 
    AVAILABLE = "AVAILABLE" #disponnible
    
    
class TimesTampMixin:
    @declared_attr
    def date_added(cls):
        return Column(DateTime, default=datetime.now())

    @declared_attr
    def date_modified(cls):
        return Column(DateTime, onupdate=datetime.now())


@event.listens_for(TimesTampMixin, 'before_insert', propagate=True)
def update_created_modified_on_create_listener(mapper, connection, target):
    target.date_added = datetime.now()
    target.date_modified = datetime.now()

@event.listens_for(TimesTampMixin, 'before_update', propagate=True)
def update_modified_on_update_listener(mapper, connection, target):
    target.date_modified = datetime.now()



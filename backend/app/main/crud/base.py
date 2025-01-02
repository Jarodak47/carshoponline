import math
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from sqlalchemy import or_,asc,desc
from sqlalchemy.orm import Session

from app.main.models.db.base_class import Base
from app.main import schemas, models


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, uuid: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == uuid,self.model.status!='DELETED').first()

    def get_multi(
            self, db: Session, *, page: int = 0, per_page: int = 20,filters: Optional[Dict[str, Any]]
    ) -> schemas.DataList:

        order_filed = filters.get('order_filed', 'date_added')
        order = filters.get('order', 'desc')
        
        try:
            query = db.query(self.model).filter(self.model.status!='DELETED')
        except:
            query = db.query(self.model)
            
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    column_attr = getattr(self.model, key)
                    query = query.filter(getattr(self.model, key) == value)
                    if isinstance(value, str):
                        query = query.filter(column_attr.ilike('%' + str(value) + '%'))
                    else:    
                        query = query.filter(column_attr == value)

            if order_filed:
                if hasattr(self.model, order_filed):    
                    if order == 'asc':
                        query = query.order_by(asc(getattr(self.model, order_filed)))
                    else:
                        query = query.order_by(desc(getattr(self.model, order_filed)))
                                  
        total = query.count()
        result = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return schemas.DataList(
            total=total,    
            pages=math.ceil(total / per_page),
            current_page=page,
            per_page=per_page,
            data=result
        )

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                print(field)
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, uuid: Any) -> ModelType:
        obj = db.query(self.model).get(uuid)
        db.delete(obj)
        db.commit()
        return obj
    
    def soft_delete(self, db: Session, *, uuid: Any) -> ModelType:
        obj = db.query(self.model).get(uuid)
        # if isinstance(uuid,list):
        #     for uuid in uuid:
        #         obj = db.query(self.model).get(uuid)
        #         obj.status = models.EnumList.DELETED
        # else:
        #     obj.status = models.EnumList.DELETED

        obj.status = models.EnumList.DELETED
        db.commit()
        return obj
    
    def slugify(cls, text:str):
        return text.lower().replace(" ","-")

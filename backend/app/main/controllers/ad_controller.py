from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("/create",summary = "create a new ad", response_model=schemas.Ad, status_code=200)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AdCreate,
    # current_user:models.User = Depends(TokenRequired(roles =['administrator'])),
)->schemas.Ad:
    """
    add a new ad
    """
    return crud.ad.create1(db, obj_in)

@router.put("", response_model=schemas.Ad, status_code=201)
def update(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AdUpdate,
    current_user:models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Ad:
    """
    Update a ad
    """
    db_obj = crud.ad.get_by_uuid(db, obj_in.uuid)
    if not db_obj:
        raise HTTPException(status_code=404, detail=__("ad-not-found"))

    return crud.ad.update1(db, obj_in,db_obj)

@router.delete("", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    uuids: list[str],
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Msg:
    """
    Delete Ad
    """
    db_obj = db.query(models.Ad).filter(models.Ad.uuid.in_(uuids)).all()

    if not db_obj or len(db_obj) != len(uuids):
        raise HTTPException(status_code=404, detail=__("ad-not-found"))
    
    crud.ad.soft_delete(db, uuids)
    return {"message": __("ad-deleted")}

@router.get("/all", response_model=schemas.AdResponseList)
def get_all(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,

    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    
    status: Optional[str] = Query(None,enum =[i.value for i in  models.EnumList]),
    order:Optional[str] = Query(None,enum =['asc', 'desc']),
    order_filed: Optional[str] = Query(None,enum =['date_added', 'date_modified'])
)->schemas.AdResponseList:
    """
    get ad with all data by passing filters
    """
    # obj_in = schemas.AdSearchRequest(
    #     brand = brand,
    #     model= model,
    #     color= color,
    #     title = year,
    #     quantity= quantity,
    #     is_rentable= is_rentable,
    #     is_purchasable= is_purchasable,
    #     is_bookable= is_bookable,
    #     status = status,
    #     order = order
    # )
    filters = {
        "title": title,
        "description": description,
        "status": status,
        "order": order,
        "order_filed": order_filed
    }    
    filters = {k: v for k, v in filters.items() if v is not None}
    
    return crud.ad.get_multi(
        db, 
        page, 
        per_page,
        obj_in = filters
    )

@router.get("/{ad_uuid}", response_model=Optional[schemas.Ad],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    ad_uuid:str
)->Optional[schemas.Ad]:
    """
    get administrator with all data by passing filters
    """
    db_obj =  crud.ad.get_by_uuid(
        db, 
        ad_uuid
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("ad-not-found"))
    
    return crud.ad.get_by_uuid(
        db, 
        ad_uuid
    )
    
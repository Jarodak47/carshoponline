from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(prefix="/brands", tags=["brands"])


@router.post("/create",summary = "add a brand", response_model=schemas.Brand, status_code=200)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.BrandCreate,
    current_user:models.User = Depends(TokenRequired(roles =['administrator'])),
)->schemas.Brand:
    """
    add a new vehicle
    """
    if obj_in.name in [i.name for i in db.query(models.Brand)]: 
        raise HTTPException(status_code=409, detail=__("brand-name-taken"))
    
    return crud.brand.create(db, obj_in)

@router.put("/{brand_uuid}", response_model=schemas.Brand, status_code=201)
def update(
    *,
    db: Session = Depends(get_db),
    brand_uuid:str,
    name:str=Body(...),
    current_user:models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Brand:
    """
    Update a vehicle
    """
    db_obj = crud.brand.get_by_uuid(db, brand_uuid)
    if not db_obj:
        raise HTTPException(status_code=404, detail=__("brand-not-found"))
    
    tab_name = db.query(models.Brand).all()
    print("tab_name11",tab_name)
    print("db_obj_name111",db_obj.name)
    if name in [i.name for i in db.query(models.Brand)] and name!= db_obj.name:
        raise HTTPException(status_code=409, detail=__("brand-name-taken"))
    
    return crud.brand.update(db, brand_uuid, name)

@router.delete("", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    uuids: list[str],
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Msg:
    """    
    Delete Vehicle
    """
    db_obj = db.query(models.Brand).filter(models.Brand.uuid.in_(uuids)).all()

    if not db_obj or len(db_obj) != len(uuids):
        raise HTTPException(status_code=404, detail=__("brand-not-found"))
    
    crud.vehicle.soft_delete(db, uuids)
    return {"message": __("brand-deleted")}


@router.delete("/{brand_uuid}", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    brand_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Msg:
    """    
    Delete Vehicle
    """

    db_obj= crud.brand.get_by_uuid(db,brand_uuid)
    if not db_obj:
        raise HTTPException(status_code=404, detail=__("brand-not-found"))
    
    db_obj.status = 'DELETED'
    db.commit()
    
    return {"message": __("brand-deleted")}

@router.get("/all", response_model=schemas.BrandResponseList)
def get_all(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,

    name: Optional[str] = Query(None),
    slug: Optional[str] = Query(None),
    status: Optional[str] = Query(None,enum =['RENTAL','PURCHASE','BOOKING']),
    order:Optional[str] = Query(None,enum =['asc', 'desc']),
    order_filed: Optional[str] = Query(None,enum =['date_added', 'date_modified'])
)->schemas.BrandResponseList:
    """
    get vehicle with all data by passing filters
    """
   
    filters = {
        "name": name,
        "slug": slug,
        "status": status,
        "order": order,
        "order_filed": order_filed
    }    
    filters = {k: v for k, v in filters.items() if v is not None}
    
    return crud.brand.get_multi(
        db, 
        page, 
        per_page,
        obj_in = filters
    )

@router.get("/{brand_uuid}", response_model=Optional[schemas.Brand],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    brand_uuid:str
)->Optional[schemas.Brand]:
    """
    get administrator with all data by passing filters
    """
    db_obj =  crud.brand.get_by_uuid(
        db, 
        brand_uuid
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("brand-not-found"))
    
    return crud.brand.get_by_uuid(
        db, 
        brand_uuid
    )

@router.get("/one/{slug}", response_model=Optional[schemas.Brand],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    slug:str
)->Optional[schemas.Brand]:
    """
    get administrator with all data by passing filters
    """

    db_obj =  crud.brand.get_by_slug(
        db, 
        slug
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("brand-not-found"))
    
    return db_obj
    
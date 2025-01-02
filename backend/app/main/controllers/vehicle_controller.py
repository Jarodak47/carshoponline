from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/create",summary = "add a vehicle", response_model=schemas.Vehicle, status_code=200)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.VehicleCreate,
    current_user:models.User = Depends(TokenRequired(roles =['administrator'])),
)->schemas.Vehicle:
    """
    add a new vehicle
    """

    if obj_in.model in [i.model for i in db.query(models.Vehicle)]: 
        raise HTTPException(status_code=409, detail=__("vehicle-model-taken"))
    return crud.vehicle.create(db, obj_in)

@router.put("", response_model=schemas.Vehicle, status_code=201)
def update(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.VehicleUpdate,
    current_user:models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Vehicle:
    """
    Update a vehicle
    """
    db_obj = crud.vehicle.get_by_uuid(db, obj_in.uuid)
    if not db_obj:
        raise HTTPException(status_code=404, detail=__("vehicle-not-found"))
    
    if obj_in.model in [db.query(models.Vehicle.model).all()] and obj_in.model!= db_obj.model:
        raise HTTPException(status_code=409, detail=__("vehicle-model-taken"))

    return crud.vehicle.update1(db, obj_in,db_obj)

@router.delete("", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    uuids: list[str],
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Msg:
    """    ad = relationship('Ad', back_populates='photos')

    Delete Vehicle
    """
    db_obj = db.query(models.Vehicle).filter(models.Vehicle.uuid.in_(uuids)).all()

    if not db_obj or len(db_obj) != len(uuids):
        raise HTTPException(status_code=404, detail=__("vehicle-not-found"))
    
    crud.vehicle.soft_delete(db, uuids)
    return {"message": __("vehicle-deleted")}

@router.delete("/{vehicle_uuid}", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    vehicle_uuid: str,
    current_user: models.User = Depends(TokenRequired(roles =["administrator"] ))
)->schemas.Msg:
    """    ad = relationship('Ad', back_populates='photos')

    Delete Vehicle
    """
    db_obj = db.query(models.Vehicle).filter(models.Vehicle.uuid==vehicle_uuid).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail=__("vehicle-not-found"))
    uuids = [vehicle_uuid]
    crud.vehicle.soft_delete(db, uuids)
    return {"message": __("vehicle-deleted")}

@router.get("/all", response_model=schemas.VehicleResponseList)
def get_all(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,

    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    
    status: Optional[str] = Query(None,enum =[i.value for i in  models.EnumList]),
    year: Optional[int] = Query(None),
    order:Optional[str] = Query(None,enum =['asc', 'desc']),
    order_filed: Optional[str] = Query(None,enum =['date_added', 'date_modified'])
)->schemas.VehicleResponseList:
    """
    get vehicle with all data by passing filters
    """
    # obj_in = schemas.VehicleSearchRequest(
    #     brand = brand,
    #     model= model,
    #     color= color,
    #     year = year,
    #     quantity= quantity,
    #     is_rentable= is_rentable,
    #     is_purchasable= is_purchasable,
    #     is_bookable= is_bookable,
    #     status = status,
    #     order = order
    # )
    filters = {
        "brand": brand,
        "model": model,
        "year": year,
        "color": color,
        "status": status,
        "order": order,
        "order_filed": order_filed
    }    
    filters = {k: v for k, v in filters.items() if v is not None}
    return crud.vehicle.get_multi(
        db, 
        page, 
        per_page,
        obj_in = filters
    )

@router.get("/{vehicle_uuid}", response_model=Optional[schemas.Vehicle],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    vehicle_uuid:str
)->Optional[schemas.Vehicle]:
    """
    get administrator with all data by passing filters
    """
    db_obj =  crud.vehicle.get_by_uuid(
        db, 
        vehicle_uuid
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("vehicle-not-found"))
    
    return db_obj

@router.get("/brand/{vehicle_uuid}/{brand_uuid}", response_model=Optional[schemas.RelatedVehicleForBrand],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    vehicle_uuid:str,
    brand_uuid:str
)->Optional[schemas.RelatedVehicleForBrand]:
    """
    get administrator with all data by passing filters
    """
    brand = crud.brand.get_by_uuid(db, brand_uuid)
    if not brand:
        raise HTTPException(status_code = 404 ,detail=__("brand-not-found"))
    
    vehicle = crud.vehicle.get_by_uuid(db, vehicle_uuid)
    if not vehicle:
        raise HTTPException(status_code = 404 ,detail=__("vehicle-not-found"))
    

    db_obj =  crud.vehicle.get_by_uuid_and_brand_uuid(
        db, 
        vehicle_uuid,
        brand_uuid
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("vehicle-not-found"))
    
    db_obj

    
    related_vehicles_in_brand:Optional[list[models.Vehicle]] = brand.vehicles
    if vehicle in related_vehicles_in_brand:
        related_vehicles_in_brand.remove(vehicle)
    
    return schemas.RelatedVehicleForBrand(
        total_count=len(related_vehicles_in_brand),
        vehicles = related_vehicles_in_brand
        
    )


@router.get("/one/{slug}", response_model=Optional[schemas.Vehicle],status_code = 200)
def get(
    *,
    db: Session = Depends(get_db),
    slug:str
)->Optional[schemas.Vehicle]:
    """
    get administrator with all data by passing filters
    """

    db_obj =  crud.vehicle.get_by_slug(
        db, 
        slug
    )

    if not db_obj:
        raise HTTPException(status_code = 404 ,detail=__("vehicle-not-found"))
    
    return db_obj
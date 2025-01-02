from app.main.core.dependencies import get_db,TokenRequired
from app.main import models,schemas
from app.main.core.i18n import __
from fastapi import APIRouter, Depends,Body,HTTPException
from typing import Any
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.orm import Session
from app.main.services.braintree_service import braintree_api_service



router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/token")
async def get_token()->str:
    """
    Get token
    """
    data = await braintree_api_service.generate_client_token()
    return data

@router.post("/create")
async def checkout_payment(
    *,
    db: Session = Depends(get_db),
    obj_in:dict[str,Any] = Body(...),
    current_user:models.User = Depends(TokenRequired(roles =[]))
):
    """
    add a new payment
    """
    amount_total = sum(item.get('price') for item in obj_in['cart'])

    new_order = models.Order(
        uuid = uuid.uuid4(),
        quantity= len(obj_in['cart']),
        total_amount= amount_total,
        buyer_uuid = current_user.uuid,
        products = jsonable_encoder(obj_in['cart'])
    )
    db.add(new_order)

    data =  await braintree_api_service.create_payment(obj_in['nonce'],amount_total)

    if data.is_success:
        new_order.status = "PROCESSING"
        payment_data = {
            "id": data.transaction.id,
            "status": data.transaction.status,
            "amount": float(data.transaction.amount), 
            "currency": data.transaction.currency_iso_code,
            "created_at": data.transaction.created_at.isoformat(),
            "updated_at": data.transaction.updated_at.isoformat(),
        #     "type": data.transaction.type,
        #     "payment_method": data.transaction.payment_instrument_type
            
        #     # Ajoutez d'autres champs nécessaires ici
        }
        new_order.payment = payment_data  # Stocker les données simplifiées dans la colonne payment    
        


    elif data.transaction:
        raise HTTPException(status_code=400, detail=data.message)
    
    else:
        new_order.status = "NOT_PROCESSED"

    db.commit()
    return  payment_data   


@router.get("/orders",response_model= list[schemas.OrderResponse] ,status_code=200)
async def get_orders(
    *,
    db: Session = Depends(get_db),
    current_user:models.User = Depends(TokenRequired(roles =[]))
)->list[schemas.OrderResponse]:
    """
    Get orders
    """
    data = db.query(models.Order).filter(models.Order.buyer_uuid == current_user.uuid).all()
    return  data

@router.put("/order-status/{order_uuid}",response_model= schemas.OrderResponse ,status_code=200)
async def get_order_status(
    *,
    db: Session = Depends(get_db),
    order_uuid:str,
    status:str,
    current_user:models.User = Depends(TokenRequired(roles =[]))
)->schemas.OrderResponse:
    """
    Get orders
    """
    order = db.query(models.Order).filter(models.Order.buyer_uuid == current_user.uuid).first()
    if not order:
        raise HTTPException(status_code=404, detail=__("order-not-found"))
    order.status = status
    db.commit()
    return  order
        


        



    
    
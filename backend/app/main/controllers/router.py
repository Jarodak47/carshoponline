from fastapi import APIRouter


from .user_controller import router as user
from .authentication_controller import router as authentication
from .migration_controller import router as migration
from .storage_controller import router as storage
from .role_controller import router as role
from .vehicle_controller import router as vehicle
from .ad_controller import router as ad
from .brand_controller import router as brand
from .payment_controller import router as payment

api_router = APIRouter()

api_router.include_router(authentication)
api_router.include_router(payment)
api_router.include_router(role)
api_router.include_router(storage)
api_router.include_router(user)
api_router.include_router(vehicle)
api_router.include_router(brand)
api_router.include_router(ad)
api_router.include_router(migration)
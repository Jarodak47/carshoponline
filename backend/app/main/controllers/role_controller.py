from app.main.core.dependencies import get_db
from app.main import schemas, crud
from app.main.core.i18n import __
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
router = APIRouter(prefix="/roles", tags=["roles"])




@router.get("", response_model=list[schemas.RoleInDB],status_code=200)
async def get_roles(
    *,
    code: str = None,
    db: Session = Depends(get_db),
    # current_user=Depends(TokenRequired())
) -> list:
    """
    Roles
    """
    return crud.role.get_all(db, code)
import json
import os
import shutil
import platform
from dataclasses import dataclass
from sqlalchemy.exc import ProgrammingError

from app.main import crud
from fastapi import APIRouter, Body, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Column, String
from app.main import schemas
from app.main.core.config import Config
from app.main.core import dependencies
from app.main.core.security import get_password_hash
from app.main.models.db.base_class import Base
from app.main.utils import logger
from app.main import models, crud
from app.main.models.base import EnumList
from app.main.core.i18n import __

router = APIRouter(prefix="/migrations", tags=["migrations"])


def check_user_access_key(admin_key: schemas.AdminKey):
    logger.info(f"Check user access key: {admin_key.key}")
    if admin_key.key not in [Config.ADMIN_KEY]:
        raise HTTPException(status_code=400, detail="Clé d'accès incorrecte")

@router.post("/create-default-data",response_model = schemas.Msg, status_code = 201)
async def create_default_data(
     db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """Create default_data"""
    check_user_access_key(admin_key)
    
    with open('{}/app/main/templates/default_data/storages.json'.format(os.getcwd()), encoding='utf-8') as f:
        datas = json.load(f)
        for data in datas:
            storage = db.query(models.Storage).filter(models.Storage.uuid == data["uuid"]).first()
            
            if not storage:
                storage = models.Storage(
                    uuid=data["uuid"],
                    url=data["url"],
                    medium=data["medium"],
                    format=data["format"],
                    thumbnail=data["thumbnail"],
                    size=data["size"],
                    mimetype=data["mimetype"],
                    file_name=data["file_name"],
                    summary = data["summary"],
                    public_id = data["public_id"],
                    cloudinary_file_name = data["cloudinary_file_name"],
                    width=data["width"],
                    height=data["height"],
                    version=data["version"],
                    
                )
                db.add(storage)
    
    with open('{}/app/main/templates/default_data/brands.json'.format(os.getcwd()), encoding='utf-8') as f:
        datas = json.load(f)

        for data in datas:
            brand = crud.brand.get_by_uuid(db=db, uuid=data["uuid"])
            if not brand:
                # crud.brand.update(db, schemas.BrandUpdate(**data))
                brand = models.Brand(
                    logo_uuid=data["logo_uuid"],
                    name=data["name"],
                    slug=data["slug"],
                    status=data["status"],
                    uuid=data["uuid"]
                )
                db.add(brand)

    with open('{}/app/main/templates/default_data/vehicles.json'.format(os.getcwd()), encoding='utf-8') as f:
        datas = json.load(f)
        for data in datas:
            vehicle = db.query(models.Vehicle).filter(models.Vehicle.uuid == data["uuid"]).first()
            if not vehicle:
                vehicle = models.Vehicle(
                    brand_uuid=data["brand_uuid"],
                    status = data["status"],
                    color=data["color"],
                    description=data["description"],
                    engineSize=data["engineSize"],
                    fuelType=data["fuelType"],
                    fuelTank=data["fuelTank"],
                    warranty=data["warranty"],
                    is_bookable=True,
                    is_purchasable=True,
                    is_rentable=True,
                    mileage=data["mileage"],
                    price=data["price"],
                    quantity=data["quantity"],
                    seater=data["seater"],
                    size=data["size"],
                    safetyrating=data["safetyrating"],
                    slug=data["slug"],
                    transmission=data["transmission"],
                    year=data["year"],
                    model=data["model"],
                    uuid=data["uuid"]
                )
                db.add(vehicle)
    
    with open('{}/app/main/templates/default_data/vehicle_images.json'.format(os.getcwd()), encoding='utf-8') as f:
        datas = json.load(f)
        for data in datas:
            vehicle_image = db.query(models.VehicleImage).filter(models.VehicleImage.uuid == data["uuid"],models.VehicleImage.image_uuid == data["image_uuid"]).first()
            if not vehicle_image:
                vehicle_image = models.VehicleImage(
                    vehicle_uuid=data["vehicle_uuid"],
                    image_uuid=data["image_uuid"],
                    uuid=data["uuid"]
                )
                db.add(vehicle_image)

    db.commit()
                
    return {"message": "Les donnees par defaut  ont été créées avec succès"}



@router.post("/create-database-tables", response_model=schemas.Msg, status_code=201)
async def create_database_tables(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create database structure (tables)
    """
    check_user_access_key(admin_key)
    """ Try to remove previous alembic tags in database """
    try:
        @dataclass
        class AlembicVersion(Base):
            __tablename__ = "alembic_version"
            version_num: str = Column(String(32), primary_key=True, unique=True)

        db.query(AlembicVersion).delete()
        db.commit()
    except Exception as e:
        pass

    """ Try to remove previous alembic versions folder """
    migrations_folder = os.path.join(os.getcwd(), "alembic", "versions")
    try:
        shutil.rmtree(migrations_folder)
    except Exception as e:
        pass

    """ create alembic versions folder content """
    try:
        os.mkdir(migrations_folder)
    except OSError:
        logger.error("Creation of the directory %s failed" % migrations_folder)
    else:
        logger.info("Successfully created the directory %s " % migrations_folder)

    try:
        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\venv\\Scripts\\python.exe -m alembic revision --autogenerate')
            os.system('set PYTHONPATH=. && .\\venv\\Scripts\\python.exe -m alembic upgrade head')

        else:
            os.system('PYTHONPATH=. alembic revision --autogenerate')
        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\.venv\Scripts\python.exe -m alembic upgrade head')

        else:
            os.system('PYTHONPATH=. alembic upgrade head')

        """ Try to remove previous alembic versions folder """
        try:
            shutil.rmtree(migrations_folder)
            pass
        except Exception as e:
            pass

        return {"message": "Les tables de base de données ont été créées avec succès"}

    except ProgrammingError as e:
        raise ProgrammingError(status_code=512, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-user-roles", response_model=schemas.Msg, status_code=201)
async def create_user_roles(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create user roles.
    """
    check_user_access_key(admin_key)
    
    try:
        with open('{}/app/main/templates/default_data/roles.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)

            for data in datas:
                user_role = crud.role.get_by_uuid(db=db, uuid=data["uuid"])
                if user_role:
                    crud.role.update(db, schemas.RoleUpdate(**data))
                else:
                    user_role = models.Role(
                        title_fr=data["title_fr"],
                        title_en=data["title_en"],
                        code=data["code"],
                        description=data["description"],
                        uuid=data["uuid"]
                    )
                    db.add(user_role)
                    db.flush
        db.commit()
        return {"message": "Les rôles ont été créés avec succès"}
        
    except IntegrityError as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=409, detail=__("user-role-conflict"))
    except Exception as e:
        db.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-admin-users", response_model=schemas.Msg, status_code=201)
async def create_admin_users(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create admins users.
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/default_data/administrator.json'.format(os.getcwd()), encoding='utf-8') as f:        
            datas = json.load(f)
            for data in datas:
                db_obj = crud.user.get_by_uuid(db=db, uuid=data["uuid"])
                if db_obj:
                    crud.user.update(db, schemas.AdministratorUpdate(
                        uuid=data['uuid'],
                        firstname=data['firstname'],
                        lastname=data['lastname'],
                        email=data['email'],
                        phonenumber=data['phonenumber'],
                        address=data['address'],
                        role_uuid=data['role_uuid'],
                        avatar_uuid=data['avatar_uuid'],
                        password_hash=get_password_hash(data['password_hash']),
                        status=data['status'],
                        date_added=data['date_added'],
                        date_modified=data['date_modified']
                        )
                    )
                    print("exist_db_obj1",db_obj)
                else:
                    # crud.administrator.create(db,schemas.AdministratorCreate(**data))
                    db_obj = models.User(
                        uuid=data["uuid"],
                        firstname=data["firstname"],
                        lastname=data["lastname"],
                        email=data['email'],
                        phonenumber=data['phonenumber'],
                        address=data['address'],
                        role_uuid=data["role_uuid"],
                        avatar_uuid=data["avatar_uuid"],
                        password_hash=get_password_hash(data["password_hash"]),
                        status=data["status"],
                        date_added=data["date_added"],
                        date_modified=data["date_modified"]
                    )
                    db.add(db_obj)
                    db.flush()
                    db.commit()
                
                print("data",data)
        return {"message": "Les administrateurs ont été créés avec succès"}
        
    except IntegrityError as e:
        logger.error(str(e))
        raise HTTPException(status_code=409, detail=__("admin-role-conflict"))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")

@router.post("/update-vehicles-slug", response_model=schemas.Msg, status_code=201)
async def update_vehicles_slug(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    update vehicles slug.
    """
    check_user_access_key(admin_key)
    
    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        vehicle.slug = crud.vehicle.slugify(vehicle.model)
        db.commit()
    return {"message": "Les véhicules ont été mis à jour avec succès"}



@router.post("/create-default-brands", response_model=schemas.Msg, status_code=201)
async def create_default_brands(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create admins users.
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/default_data/administrator.json'.format(os.getcwd()), encoding='utf-8') as f:        
            datas = json.load(f)
            for data in datas:
                db_obj = crud.user.get_by_uuid(db=db, uuid=data["uuid"])
                if db_obj:
                    crud.user.update(db, schemas.AdministratorUpdate(
                        uuid=data['uuid'],
                        firstname=data['firstname'],
                        lastname=data['lastname'],
                        email=data['email'],
                        phonenumber=data['phonenumber'],
                        address=data['address'],
                        role_uuid=data['role_uuid'],
                        avatar_uuid=data['avatar_uuid'],
                        password_hash=get_password_hash(data['password_hash']),
                        status=data['status'],
                        date_added=data['date_added'],
                        date_modified=data['date_modified']
                        )
                    )
                    print("exist_db_obj1",db_obj)
                else:
                    # crud.administrator.create(db,schemas.AdministratorCreate(**data))
                    db_obj = models.User(
                        uuid=data["uuid"],
                        firstname=data["firstname"],
                        lastname=data["lastname"],
                        email=data['email'],
                        phonenumber=data['phonenumber'],
                        address=data['address'],
                        role_uuid=data["role_uuid"],
                        avatar_uuid=data["avatar_uuid"],
                        password_hash=get_password_hash(data["password_hash"]),
                        status=data["status"],
                        date_added=data["date_added"],
                        date_modified=data["date_modified"]
                    )
                    db.add(db_obj)
                    db.flush()
                    db.commit()
                
                print("data",data)
        return {"message": "Les administrateurs ont été créés avec succès"}
        
    except IntegrityError as e:
        logger.error(str(e))
        raise HTTPException(status_code=409, detail=__("admin-role-conflict"))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


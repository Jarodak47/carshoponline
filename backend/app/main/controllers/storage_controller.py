from datetime import date, datetime
import os
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.main import models
from app.main.core import dependencies
from app.main.core.config import Config
from app.main.core.i18n import __
from app.main.schemas.file import StorageCreate,FileSlim,FileList,OpenAIUploadFile
from app.main.crud.storage_crud import storage
from app.main.schemas.msg import Msg
from app.main.utils.file import file_utils
import uuid
from app.main.utils.uploads import download_and_save_file, get_access_control, get_file_url, update_access_control, upload_to_cloudinary

MAX_TOKENS = 4096

router = APIRouter(
    prefix="/storages",
    tags=["storages"]
)

@router.post("/upload",response_model = FileSlim, status_code=200)
def upload_file(
        *,
        db: Session = Depends(dependencies.get_db),
        file: UploadFile = File(...),
        # current_user: models.User = Depends(dependencies.TokenRequired(roles=["administrator"]))
):
    """
    Upload a file.
    """
    try:
        # Save the file temporarily
        temp_file_path = file_utils.save_temp_file(file)
        
        # Upload to Cloudinary
        public_id = str(uuid.uuid4())
        upload_result = upload_to_cloudinary(temp_file_path, public_id)

        # Delete the temporary file
        file_utils.delete_temp_file(temp_file_path)

        # Prepare file data for database
        file_data = StorageCreate(
            uuid = str(uuid.uuid4()),
            file_name=file.filename,
            cloudinary_file_name=upload_result.get("original_filename"),
            url=upload_result.get("secure_url"),
            mimetype=f"{upload_result.get('resource_type')}/{upload_result.get('format')}",
            format=upload_result.get("format"),
            public_id=upload_result.get("public_id"),
            version=upload_result.get("version"),
            width=upload_result.get("width"),
            height=upload_result.get("height"),
            size=upload_result.get("bytes"),
        )

        # Store file data in the database
        stored_file = storage.store_file(db, file_data)

        return stored_file
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/get/{public_id}", status_code=200)
def get_file(
    *,
    public_id: str, 
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.TokenRequired())

    ):
    """
    Get file from Cloudinary
    """
    # Retrieve file metadata from the database
    file_record = storage.get_file_by_public_id(db=db, public_id=public_id)
    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
        
    url = get_file_url(public_id = file_record.public_id)
    if not url:  # If the file doesn't exist in Cloudinary
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    # Generate the secure URL for the file
    return  {
        "url": url,
        "public_id": public_id
    }



@router.get("/{public_id}/get", status_code=200)
def get_file(
    *,
    public_id: str, 
    db: Session = Depends(dependencies.get_db),
    # current_user: models.User = Depends(dependencies.TokenRequired())

    ):
    """
    Get file from Cloudinary
    """
    # Retrieve file metadata from the database
    file_record = storage.get_file_by_public_id(db, public_id)
    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    # Generate the secure URL for the file
    url = get_file_url(file_record.public_id)
    if not url:  # If the file doesn't exist in Cloudinary
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return RedirectResponse(url = url)
    
        
@router.get("/documents",response_model = FileList, status_code=200)
def get_files(
    *,
    public_id: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    per_page: int = 30,
    order:str = "desc",
    order_filed:str = "date_added",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    # date_added: Optional[date] = None,  # to filter by date_added in the range (start_date, end_date)
    document_type:Optional[str]=None,
    db: Session = Depends(dependencies.get_db)
    ):

    """
    Get files with pagination by passing filters
    """
    
    return storage.get_files(
        db = db,
        public_id=public_id,
        keyword=keyword,
        page=page,
        per_page=per_page,
        order=order,
        order_filed=order_filed,
        start_date=start_date,
        end_date=end_date,
        document_type=document_type,
        # date_added=date_added,  # to filter by date_added in the range (start_date, end_date)
    )

@router.delete("",response_model = Msg, status_code=200)
async def delete(
    *,
    file_public_id:str,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.TokenRequired(roles =["administrator"]))

    ):

    """
    delete document
    """
    # Retrieve file metadata from the database
    file_record = storage.get_file_by_public_id(db, file_public_id)
    db.delete(file_record)
    db.commit()
    return {"message": __("document-deleted-successfully")}
    
    

    

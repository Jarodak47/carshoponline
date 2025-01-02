import os

from pydantic import EmailStr
from pydantic_settings import BaseSettings
from typing import Optional


def get_secret(secret_name, default):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return os.getenv(secret_name, default)


class ConfigClass(BaseSettings):
    SECRET_KEY: str = get_secret("SECRET_KEY", 'nothing')
    ALGORITHM: str = get_secret("ALGORITHM", 'HS256')

    ADMIN_KEY: str = get_secret("ADMIN_KEY", "autobbr24")
    ADMIN_USERNAME: str = get_secret("ADMIN_USERNAME", "autobbr24")
    ADMIN_PASSWORD: str = get_secret("ADMIN_PASSWORD", "test1234")

    PROJECT_NAME: str = get_secret("PROJECT_NAME", "AUTO BUY & BOOKING & RENTAL API")
    PROJECT_VERSION: str = get_secret("PROJECT_VERSION", "0.0.1")
    PREFERRED_LANGUAGE: str = get_secret("PREFERRED_LANGUAGE", 'fr')
    API_STR: str = get_secret("API_STR", "/api/v1")

    # 60 minutes * 24 hours * 355 days = 365 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_secret("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 365))


    # Sqlalchemy
    SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL",'postgresql://postgres:postgres@localhost:5432/test_autolocate')
    # SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL", 'postgresql://postgres:postgres@localhost:5432/archive_doc_app')
    SQLALCHEMY_POOL_SIZE: int = 100
    SQLALCHEMY_MAX_OVERFLOW: int = 0
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = get_secret("SQLALCHEMY_POOL_RECYCLE", 3600)
    SQLALCHEMY_POOL_PRE_PING: bool = get_secret("SQLALCHEMY_POOL_PRE_PING", True)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
    }
    
    CLOUDINARY_CLOUD_NAME:str = get_secret("CLOUDINARY_NAME","dx3yzffmf")
    CLOUDINARY_API_KEY:str = get_secret("CLOUDINARY_API_KEY","911872347119858")
    CLOUDINARY_API_SECRET:str = get_secret("CLOUDINARY_API_SECRET","jxY5Se-oJJTboooIWlSh75hMgmg")
    CLOUDINARY_API_SECURE:bool = get_secret("CLOUDINARY_API_SECURE", True)
    # CLOUDINARY_SECURE_URL:str = get_secret("CLOUDINARY_SECURE_URL", "https://console.cloudinary.com/console/c-c88740024fb4dd0748e39b70bb9789/media_library/search/asset/{}/manage?q=&view_mode=mosaic&context=manage")
    # CLOUDINARY_URL:str=f"cloudinary://{CLOUDINARY_API_KEY}:{CLOUDINARY_API_SECRET}@{CLOUDINARY_CLOUD_NAME}"
    
    LOCAL: bool = os.getenv("LOCAL", True)

    SMTP_TLS: bool = get_secret("SMTP_TLS", True)
    SMTP_SSL: bool = get_secret("SMTP_SSL", False)
    SMTP_PORT: Optional[int] = int(get_secret("SMTP_PORT", 587))
    SMTP_HOST: Optional[str] = get_secret("SMTP_HOST", "smtp.gmail.com")
    SMTP_USER: Optional[str] = get_secret("SMTP_USER", "jarodak47@gmail.com")
    SMTP_PASSWORD: Optional[str] = get_secret("SMTP_PASSWORD", "zzhuazeaoakqgvls")
    EMAILS_FROM_EMAIL: Optional[EmailStr] = get_secret("EMAILS_FROM_EMAIL", "jarodak47@gmail.com")
    EMAILS_FROM_NAME: Optional[str] = get_secret("EMAILS_FROM_NAME", "AUTO BUY & BOOKING & RENTAL APP")

    EMAIL_TEMPLATES_DIR: str = "{}/app/main/templates/emails/render".format(os.getcwd())
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = int(get_secret("EMAIL_RESET_TOKEN_EXPIRE_HOURS", 48))
    EMAILS_ENABLED: bool = get_secret("EMAILS_ENABLED", True) in ["True", True]

    # RESET_PASSWORD_LINK: str = get_secret("RESET_PASSWORD_LINK", "https://app.development.koalizz.fr/{}/auth/reset-password")

    # Default image size
    IMAGE_MEDIUM_WIDTH: int = get_secret("IMAGE_MEDIUM_WIDTH", 600)
    IMAGE_THUMBNAIL_WIDTH: int = get_secret("IMAGE_THUMBNAIL_WIDTH", 300)

    UPLOADED_FILE_DEST: str = get_secret("UPLOADED_FILE_DEST", "uploads")

    BRAINTREE_MERCHANT_ID: str = get_secret("BRAINTREE_MERCHANT_ID", "mdrfb3r4g663vhwd")
    BRAINTREE_PUBLIC_KEY: str = get_secret("BRAINTREE_PUBLIC_KEY", "f4gr5f2vrfmxzsfp")
    BRAINTREE_PRIVATE_KEY: str = get_secret("BRAINTREE_PRIVATE_KEY", "5ac4d23220e51863f5a57a829152f8c1")
    BRAINTREE_ENVIRONMENT: str = get_secret("BRAINTREE_ENVIRONMENT", "sandbox")  # ou "production"


    class Config:
        case_sensitive = True


Config = ConfigClass()
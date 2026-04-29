from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # SharePoint
    SHAREPOINT_URL: str

    # Modo App Registration (produção)
    CLIENT_ID:     Optional[str] = None
    CLIENT_SECRET: Optional[str] = None
    TENANT_ID:     Optional[str] = None

    # Modo usuário (desenvolvimento)
    SP_USERNAME: Optional[str] = None
    SP_PASSWORD: Optional[str] = None

    # App
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
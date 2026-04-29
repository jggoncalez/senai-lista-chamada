from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SHAREPOINT_URL: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    TENANT_ID: str
    

    class Config:
        env_file = ".env"
        
settings = Settings()

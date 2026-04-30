from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SHAREPOINT_URL: str

    CLIENT_ID: str | None = None
    CLIENT_SECRET: str | None = None
    TENANT_ID: str | None = None

    SP_USERNAME: str | None = None
    SP_PASSWORD: str | None = None

    DEVICE_FLOW_CLIENT_ID: str = "9bc3ab49-b65d-410a-85ad-de819febfddc"
    DEVICE_FLOW_TENANT: str | None = None

    ALUNOS_LIST_NAME: str = "lst_alunos"
    CHAMADAS_LIST_NAME: str = "lst_presenca_alunos"

    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]


settings = Settings()
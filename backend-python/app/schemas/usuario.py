from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nome: str
    email: str
    role_id: int
    azure_object_id: Optional[str] = None
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    azure_object_id: Optional[str] = None
    ativo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

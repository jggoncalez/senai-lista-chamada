from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CursoBase(BaseModel):
    nome: str
    carga_horaria: int
    eixo_tecnologico: Optional[str] = None
    duracao_termos: int
    ativo: bool = True


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None
    eixo_tecnologico: Optional[str] = None
    duracao_termos: Optional[int] = None
    ativo: Optional[bool] = None


class CursoResponse(CursoBase):
    id: int
    criado_em: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

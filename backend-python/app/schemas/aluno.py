from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AlunoBase(BaseModel):
    turma_id: int
    nome: str
    empresa: Optional[str] = None
    ra: Optional[str] = None
    chamada: Optional[int] = None
    ativo: bool = True


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    turma_id: Optional[int] = None
    nome: Optional[str] = None
    empresa: Optional[str] = None
    ra: Optional[str] = None
    chamada: Optional[int] = None
    ativo: Optional[bool] = None


class AlunoResponse(AlunoBase):
    id: int
    turma: Optional[str] = None
    cod_turma: Optional[str] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AlunoImport(BaseModel):
    nome: str
    turma: str
    cod_turma: str
    chamada: Optional[int] = None
    termo: Optional[int] = None

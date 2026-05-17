from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TurmaBase(BaseModel):
    cod_turma: Optional[str] = None
    nome_turma: str
    curso_id: Optional[int] = None
    termo: int
    ativo: bool = True


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    cod_turma: Optional[str] = None
    nome_turma: Optional[str] = None
    curso_id: Optional[int] = None
    termo: Optional[int] = None
    ativo: Optional[bool] = None


class TurmaResponse(TurmaBase):
    id: int
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

from app.schemas.aluno import AlunoResponse


class SessaoAulaBase(BaseModel):
    turma_disciplina_id: int
    professor_id: int
    data_aula: date
    observacao: Optional[str] = None


class SessaoAulaCreate(SessaoAulaBase):
    pass


class SessaoAulaUpdate(BaseModel):
    observacao: Optional[str] = None


class SessaoAulaResponse(SessaoAulaBase):
    id: int
    registrado_em: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AlunosSessaoResponse(BaseModel):
    alunos_turma: list[AlunoResponse]
    alunos_extra: list[AlunoResponse]

    model_config = ConfigDict(from_attributes=True)

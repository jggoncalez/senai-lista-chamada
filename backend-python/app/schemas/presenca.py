from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class PresencaBase(BaseModel):
    sessao_id: int
    aluno_id: int
    faltas: int
    observacao: Optional[str] = None


class PresencaCreate(PresencaBase):
    pass


class PresencaUpdate(BaseModel):
    faltas: Optional[int] = None
    observacao: Optional[str] = None


class PresencaResponse(PresencaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ChamadaLoteItem(BaseModel):
    aluno_id: int
    faltas: int
    observacao: Optional[str] = None


class ChamadaLoteCreate(BaseModel):
    sessao_id: int
    presencas: list[ChamadaLoteItem]

class ChamadaRelatorioResponse(BaseModel):
    id: Optional[int] = None
    nome_aluno: str
    cod_turma: Optional[str] = None
    chamada: Optional[int] = None
    data_aula: date
    disciplina: str
    faltas: int

    model_config = ConfigDict(from_attributes=True)

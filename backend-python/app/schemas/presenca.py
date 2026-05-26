from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class PresencaBase(BaseModel):
    sessao_id: int
    aluno_id: int
    presente: bool
    observacao: Optional[str] = None


class PresencaCreate(PresencaBase):
    pass


class PresencaUpdate(BaseModel):
    presente: Optional[bool] = None
    observacao: Optional[str] = None


class PresencaResponse(PresencaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ChamadaLoteItem(BaseModel):
    aluno_id: int
    presente: bool
    observacao: Optional[str] = None


class ChamadaLoteCreate(BaseModel):
    sessao_id: int
    presencas: list[ChamadaLoteItem]

class ChamadaRelatorioResponse(BaseModel):
    id: Optional[int] = None
    nome_aluno: str
    cod_turma: str
    chamada: Optional[int] = None
    data_aula: date
    disciplina: str
    presente: bool

    model_config = ConfigDict(from_attributes=True)

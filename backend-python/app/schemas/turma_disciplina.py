from pydantic import BaseModel, ConfigDict
from typing import Optional


class TurmaDisciplinaBase(BaseModel):
    turma_id: int
    curso_id: int
    professor_id: Optional[int] = None
    dia_semana: Optional[int] = None
    ativo: bool = True


class TurmaDisciplinaCreate(TurmaDisciplinaBase):
    pass


class TurmaDisciplinaUpdate(BaseModel):
    professor_id: Optional[int] = None
    dia_semana: Optional[int] = None
    ativo: Optional[bool] = None


class TurmaDisciplinaResponse(TurmaDisciplinaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

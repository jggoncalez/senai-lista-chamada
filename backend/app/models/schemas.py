from datetime import date
from pydantic import BaseModel


class AlunoCreate(BaseModel):
    nome: str
    turma: str
    cod_turma: str
    chamada: int | None = None


class AlunoUpdate(BaseModel):
    nome: str | None = None
    turma: str | None = None
    cod_turma: str | None = None
    chamada: int | None = None


class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: str
    cod_turma: str
    chamada: int | None = None


class ChamadaCreate(BaseModel):
    nome_aluno: str
    cod_turma: str
    data_aula: date
    disciplina: str
    presente: bool


class ChamadaUpdate(BaseModel):
    presente: bool


class ChamadaResponse(BaseModel):
    id: int | None
    presente: bool
from pydantic import BaseModel


class ChamadaCreate(BaseModel):
    nome_aluno: str
    cod_turma: str
    data_aula: str  # formato ISO: 2026-04-29
    disciplina: str
    presente: bool


class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: str
    cod_turma: str
    chamada: int
    termo: int
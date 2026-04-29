from pydantic import BaseModel
from typing import Optional

# TO-DO: Atualizar com campos das listas do sharepoint
class ChamadaCreate(BaseModel):
    data_aula:  str
    disciplina: str
    presente:   bool

class AlunoResponse(BaseModel):
    nome:      str
    turma:     str
    n_chamada: int
    termo:     int
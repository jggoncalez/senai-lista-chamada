from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoResponse
from app.services import aluno_service

router = APIRouter(prefix="/alunos", tags=["alunos"])


@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(
    turma_id: Optional[int] = None,
    apenas_ativos: bool = True,
    db: Session = Depends(get_db),
):
    return aluno_service.listar(db, turma_id, apenas_ativos)


@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return aluno_service.buscar(db, aluno_id)


@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(dados: AlunoCreate, db: Session = Depends(get_db)):
    return aluno_service.criar(db, dados)


@router.patch("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: AlunoUpdate, db: Session = Depends(get_db)):
    return aluno_service.atualizar(db, aluno_id, dados)


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def desativar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno_service.desativar(db, aluno_id)

from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.sessao_aula import (
    SessaoAulaCreate,
    SessaoAulaUpdate,
    SessaoAulaResponse,
    AlunosSessaoResponse,
)
from app.services import sessao_aula_service

router = APIRouter(prefix="/sessoes", tags=["sessoes"])


@router.get("/", response_model=list[SessaoAulaResponse])
def listar(
    turma_disciplina_id: Optional[int] = None,
    data_aula: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return sessao_aula_service.listar(db, turma_disciplina_id, data_aula)


@router.get("/{sessao_id}", response_model=SessaoAulaResponse)
def buscar(sessao_id: int, db: Session = Depends(get_db)):
    return sessao_aula_service.buscar(db, sessao_id)


@router.get("/{sessao_id}/alunos", response_model=AlunosSessaoResponse)
def alunos_da_sessao(sessao_id: int, db: Session = Depends(get_db)):
    return sessao_aula_service.alunos_da_sessao(db, sessao_id)


@router.post("/", response_model=SessaoAulaResponse)
def criar_ou_buscar(dados: SessaoAulaCreate, db: Session = Depends(get_db)):
    return sessao_aula_service.criar_ou_buscar(db, dados)


@router.patch("/{sessao_id}", response_model=SessaoAulaResponse)
def atualizar(sessao_id: int, dados: SessaoAulaUpdate, db: Session = Depends(get_db)):
    return sessao_aula_service.atualizar(db, sessao_id, dados)

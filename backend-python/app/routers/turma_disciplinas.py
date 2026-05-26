from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.turma_disciplina import (
    TurmaDisciplinaCreate,
    TurmaDisciplinaUpdate,
    TurmaDisciplinaResponse,
)
from app.services import turma_disciplina_service

router = APIRouter(prefix="/turma-disciplinas", tags=["turma-disciplinas"])


@router.get("/hoje", response_model=list[TurmaDisciplinaResponse])
def listar_hoje(db: Session = Depends(get_db)):
    dia_semana = datetime.today().weekday()
    return turma_disciplina_service.listar(db, dia_semana=dia_semana)


@router.get("/", response_model=list[TurmaDisciplinaResponse])
def listar(
    turma_id: Optional[int] = None,
    dia_semana: Optional[int] = None,
    apenas_ativas: bool = True,
    db: Session = Depends(get_db),
):
    return turma_disciplina_service.listar(db, turma_id, dia_semana, apenas_ativas)


@router.get("/{td_id}", response_model=TurmaDisciplinaResponse)
def buscar(td_id: int, db: Session = Depends(get_db)):
    return turma_disciplina_service.buscar(db, td_id)


@router.post("/", response_model=TurmaDisciplinaResponse, status_code=status.HTTP_201_CREATED)
def criar(dados: TurmaDisciplinaCreate, db: Session = Depends(get_db)):
    return turma_disciplina_service.criar(db, dados)


@router.patch("/{td_id}", response_model=TurmaDisciplinaResponse)
def atualizar(td_id: int, dados: TurmaDisciplinaUpdate, db: Session = Depends(get_db)):
    return turma_disciplina_service.atualizar(db, td_id, dados)


@router.delete("/{td_id}", status_code=status.HTTP_204_NO_CONTENT)
def desativar(td_id: int, db: Session = Depends(get_db)):
    turma_disciplina_service.desativar(db, td_id)

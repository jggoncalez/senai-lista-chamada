from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.turma import TurmaCreate, TurmaUpdate, TurmaResponse
from app.services import turma_service

router = APIRouter(prefix="/turmas", tags=["turmas"])


@router.get("/", response_model=list[TurmaResponse])
def listar_turmas(apenas_ativas: bool = True, db: Session = Depends(get_db)):
    return turma_service.listar(db, apenas_ativas)


@router.get("/{turma_id}", response_model=TurmaResponse)
def buscar_turma(turma_id: int, db: Session = Depends(get_db)):
    return turma_service.buscar(db, turma_id)


@router.post("/", response_model=TurmaResponse, status_code=status.HTTP_201_CREATED)
def criar_turma(dados: TurmaCreate, db: Session = Depends(get_db)):
    return turma_service.criar(db, dados)


@router.patch("/{turma_id}", response_model=TurmaResponse)
def atualizar_turma(turma_id: int, dados: TurmaUpdate, db: Session = Depends(get_db)):
    return turma_service.atualizar(db, turma_id, dados)


@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
def desativar_turma(turma_id: int, db: Session = Depends(get_db)):
    turma_service.desativar(db, turma_id)

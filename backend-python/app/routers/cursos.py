from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.curso import CursoCreate, CursoUpdate, CursoResponse
from app.services import curso_service

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.get("/", response_model=list[CursoResponse])
def listar_cursos(apenas_ativos: bool = True, db: Session = Depends(get_db)):
    return curso_service.listar(db, apenas_ativos)


@router.get("/{curso_id}", response_model=CursoResponse)
def buscar_curso(curso_id: int, db: Session = Depends(get_db)):
    return curso_service.buscar(db, curso_id)


@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def criar_curso(dados: CursoCreate, db: Session = Depends(get_db)):
    return curso_service.criar(db, dados)


@router.patch("/{curso_id}", response_model=CursoResponse)
def atualizar_curso(curso_id: int, dados: CursoUpdate, db: Session = Depends(get_db)):
    return curso_service.atualizar(db, curso_id, dados)


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def desativar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso_service.desativar(db, curso_id)

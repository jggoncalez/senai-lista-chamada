from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoUpdate


def listar(db: Session, apenas_ativos: bool = True) -> list[Curso]:
    q = db.query(Curso)
    if apenas_ativos:
        q = q.filter(Curso.ativo == True)
    return q.all()


def buscar(db: Session, curso_id: int) -> Curso:
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso


def criar(db: Session, dados: CursoCreate) -> Curso:
    curso = Curso(**dados.model_dump())
    try:
        db.add(curso)
        db.commit()
        db.refresh(curso)
        return curso
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, curso_id: int, dados: CursoUpdate) -> Curso:
    curso = buscar(db, curso_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return curso
    for campo, valor in campos.items():
        setattr(curso, campo, valor)
    try:
        db.commit()
        db.refresh(curso)
        return curso
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, curso_id: int) -> None:
    curso = buscar(db, curso_id)
    curso.ativo = False
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

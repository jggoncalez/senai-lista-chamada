from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.aluno import Aluno
from app.schemas.aluno import AlunoCreate, AlunoUpdate


def listar(db: Session, turma_id: int | None = None, apenas_ativos: bool = True) -> list[Aluno]:
    q = db.query(Aluno)
    if apenas_ativos:
        q = q.filter(Aluno.ativo == True)
    if turma_id is not None:
        q = q.filter(Aluno.turma_id == turma_id)
    return q.all()


def buscar(db: Session, aluno_id: int) -> Aluno:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def criar(db: Session, dados: AlunoCreate) -> Aluno:
    if dados.ra:
        existente = db.query(Aluno).filter(Aluno.ra == dados.ra).first()
        if existente:
            raise HTTPException(status_code=409, detail="RA já cadastrado")
    aluno = Aluno(**dados.model_dump())
    try:
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        return aluno
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, aluno_id: int, dados: AlunoUpdate) -> Aluno:
    aluno = buscar(db, aluno_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return aluno
    if "ra" in campos and campos["ra"] != aluno.ra and campos["ra"] is not None:
        existente = db.query(Aluno).filter(Aluno.ra == campos["ra"]).first()
        if existente:
            raise HTTPException(status_code=409, detail="RA já cadastrado")
    campos["atualizado_em"] = datetime.utcnow()
    for campo, valor in campos.items():
        setattr(aluno, campo, valor)
    try:
        db.commit()
        db.refresh(aluno)
        return aluno
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, aluno_id: int) -> None:
    aluno = buscar(db, aluno_id)
    aluno.ativo = False
    aluno.atualizado_em = datetime.utcnow()
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

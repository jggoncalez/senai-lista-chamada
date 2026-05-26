from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.turma import Turma
from app.schemas.turma import TurmaCreate, TurmaUpdate


def listar(db: Session, apenas_ativas: bool = True) -> list[Turma]:
    q = db.query(Turma)
    if apenas_ativas:
        q = q.filter(Turma.ativo == True)
    return q.all()


def buscar(db: Session, turma_id: int) -> Turma:
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma


def criar(db: Session, dados: TurmaCreate) -> Turma:
    if dados.cod_turma:
        existente = db.query(Turma).filter(Turma.cod_turma == dados.cod_turma).first()
        if existente:
            raise HTTPException(status_code=409, detail="cod_turma já existe")
    turma = Turma(**dados.model_dump())
    try:
        db.add(turma)
        db.commit()
        db.refresh(turma)
        return turma
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, turma_id: int, dados: TurmaUpdate) -> Turma:
    turma = buscar(db, turma_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return turma
    if "cod_turma" in campos and campos["cod_turma"] != turma.cod_turma:
        existente = db.query(Turma).filter(Turma.cod_turma == campos["cod_turma"]).first()
        if existente:
            raise HTTPException(status_code=409, detail="cod_turma já existe")
    campos["atualizado_em"] = datetime.utcnow()
    for campo, valor in campos.items():
        setattr(turma, campo, valor)
    try:
        db.commit()
        db.refresh(turma)
        return turma
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, turma_id: int) -> None:
    turma = buscar(db, turma_id)
    turma.ativo = False
    turma.atualizado_em = datetime.utcnow()
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

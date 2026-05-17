from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.turma_disciplina import TurmaDisciplina
from app.schemas.turma_disciplina import TurmaDisciplinaCreate, TurmaDisciplinaUpdate


def listar(
    db: Session,
    turma_id: int | None = None,
    dia_semana: int | None = None,
    apenas_ativas: bool = True,
) -> list[TurmaDisciplina]:
    q = db.query(TurmaDisciplina)
    if apenas_ativas:
        q = q.filter(TurmaDisciplina.ativo == True)
    if turma_id is not None:
        q = q.filter(TurmaDisciplina.turma_id == turma_id)
    if dia_semana is not None:
        q = q.filter(TurmaDisciplina.dia_semana == dia_semana)
    return q.all()


def buscar(db: Session, td_id: int) -> TurmaDisciplina:
    td = db.query(TurmaDisciplina).filter(TurmaDisciplina.id == td_id).first()
    if not td:
        raise HTTPException(status_code=404, detail="Turma-disciplina não encontrada")
    return td


def criar(db: Session, dados: TurmaDisciplinaCreate) -> TurmaDisciplina:
    existente = (
        db.query(TurmaDisciplina)
        .filter(
            TurmaDisciplina.turma_id == dados.turma_id,
            TurmaDisciplina.curso_id == dados.curso_id,
            TurmaDisciplina.dia_semana == dados.dia_semana,
        )
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe essa disciplina para esta turma neste dia da semana",
        )
    td = TurmaDisciplina(**dados.model_dump())
    try:
        db.add(td)
        db.commit()
        db.refresh(td)
        return td
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, td_id: int, dados: TurmaDisciplinaUpdate) -> TurmaDisciplina:
    td = buscar(db, td_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return td
    for campo, valor in campos.items():
        setattr(td, campo, valor)
    try:
        db.commit()
        db.refresh(td)
        return td
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, td_id: int) -> None:
    td = buscar(db, td_id)
    td.ativo = False
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

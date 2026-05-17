from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.presenca import PresencaAluno
from app.models.sessao_aula import SessaoAula
from app.schemas.presenca import PresencaCreate, PresencaUpdate, ChamadaLoteItem


def buscar(db: Session, presenca_id: int) -> PresencaAluno:
    presenca = db.query(PresencaAluno).filter(PresencaAluno.id == presenca_id).first()
    if not presenca:
        raise HTTPException(status_code=404, detail="Registro de presença não encontrado")
    return presenca


def registrar(db: Session, dados: PresencaCreate) -> PresencaAluno:
    _verificar_sessao(db, dados.sessao_id)
    existente = (
        db.query(PresencaAluno)
        .filter(
            PresencaAluno.sessao_id == dados.sessao_id,
            PresencaAluno.aluno_id == dados.aluno_id,
        )
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Presença já registrada para este aluno nesta sessão",
        )
    presenca = PresencaAluno(**dados.model_dump())
    try:
        db.add(presenca)
        db.commit()
        db.refresh(presenca)
        return presenca
    except Exception:
        db.rollback()
        raise


def registrar_lote(
    db: Session, sessao_id: int, items: list[ChamadaLoteItem]
) -> list[PresencaAluno]:
    _verificar_sessao(db, sessao_id)
    resultado = []
    try:
        for item in items:
            existente = (
                db.query(PresencaAluno)
                .filter(
                    PresencaAluno.sessao_id == sessao_id,
                    PresencaAluno.aluno_id == item.aluno_id,
                )
                .first()
            )
            if existente:
                existente.presente = item.presente
                if item.observacao is not None:
                    existente.observacao = item.observacao
                resultado.append(existente)
            else:
                presenca = PresencaAluno(
                    sessao_id=sessao_id,
                    aluno_id=item.aluno_id,
                    presente=item.presente,
                    observacao=item.observacao,
                )
                db.add(presenca)
                resultado.append(presenca)
        db.commit()
        for p in resultado:
            db.refresh(p)
        return resultado
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, presenca_id: int, dados: PresencaUpdate) -> PresencaAluno:
    presenca = buscar(db, presenca_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return presenca
    for campo, valor in campos.items():
        setattr(presenca, campo, valor)
    try:
        db.commit()
        db.refresh(presenca)
        return presenca
    except Exception:
        db.rollback()
        raise


def listar_por_sessao(db: Session, sessao_id: int) -> list[PresencaAluno]:
    _verificar_sessao(db, sessao_id)
    return (
        db.query(PresencaAluno)
        .filter(PresencaAluno.sessao_id == sessao_id)
        .all()
    )


def _verificar_sessao(db: Session, sessao_id: int) -> None:
    sessao = db.query(SessaoAula).filter(SessaoAula.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão de aula não encontrada")

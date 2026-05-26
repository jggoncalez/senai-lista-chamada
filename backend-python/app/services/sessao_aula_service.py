from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sessao_aula import SessaoAula
from app.models.turma_disciplina import TurmaDisciplina
from app.models.aluno import Aluno
from app.models.aluno_disciplina_extra import AlunoDisciplinaExtra
from app.schemas.sessao_aula import SessaoAulaCreate, SessaoAulaUpdate


def listar(
    db: Session,
    turma_disciplina_id: int | None = None,
    data_aula: date | None = None,
) -> list[SessaoAula]:
    q = db.query(SessaoAula)
    if turma_disciplina_id is not None:
        q = q.filter(SessaoAula.turma_disciplina_id == turma_disciplina_id)
    if data_aula is not None:
        q = q.filter(SessaoAula.data_aula == data_aula)
    return q.all()


def buscar(db: Session, sessao_id: int) -> SessaoAula:
    sessao = db.query(SessaoAula).filter(SessaoAula.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão de aula não encontrada")
    return sessao


def criar_ou_buscar(db: Session, dados: SessaoAulaCreate) -> SessaoAula:
    existente = (
        db.query(SessaoAula)
        .filter(
            SessaoAula.turma_disciplina_id == dados.turma_disciplina_id,
            SessaoAula.data_aula == dados.data_aula,
        )
        .first()
    )
    if existente:
        return existente

    sessao = SessaoAula(**dados.model_dump())
    try:
        db.add(sessao)
        db.commit()
        db.refresh(sessao)
        return sessao
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, sessao_id: int, dados: SessaoAulaUpdate) -> SessaoAula:
    sessao = buscar(db, sessao_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return sessao
    for campo, valor in campos.items():
        setattr(sessao, campo, valor)
    try:
        db.commit()
        db.refresh(sessao)
        return sessao
    except Exception:
        db.rollback()
        raise


def alunos_da_sessao(db: Session, sessao_id: int) -> dict:
    sessao = buscar(db, sessao_id)
    td = db.query(TurmaDisciplina).filter(TurmaDisciplina.id == sessao.turma_disciplina_id).first()

    alunos_turma = (
        db.query(Aluno)
        .filter(Aluno.turma_id == td.turma_id, Aluno.ativo == True)
        .all()
    )

    ids_turma = {a.id for a in alunos_turma}

    alunos_extra = (
        db.query(Aluno)
        .join(AlunoDisciplinaExtra, AlunoDisciplinaExtra.aluno_id == Aluno.id)
        .filter(
            AlunoDisciplinaExtra.curso_id == td.curso_id,
            AlunoDisciplinaExtra.ativo == True,
            Aluno.ativo == True,
            ~Aluno.id.in_(ids_turma),
        )
        .all()
    )

    return {"alunos_turma": alunos_turma, "alunos_extra": alunos_extra}

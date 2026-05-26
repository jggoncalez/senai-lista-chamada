from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoResponse, AlunoImport
from app.services import aluno_service

router = APIRouter(prefix="/alunos", tags=["alunos"])


@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(
    turma: Optional[str] = None,
    apenas_ativos: bool = True,
    db: Session = Depends(get_db),
):
    return aluno_service.listar(db, turma, apenas_ativos)


@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    # Nota: aluno_service.buscar retorna Aluno model, 
    # AlunoResponse vai precisar de mapeamento se quisermos turma/cod_turma aqui também.
    # Por simplicidade, vamos usar o mesmo mapeamento do listar se necessário.
    aluno = aluno_service.buscar(db, aluno_id)
    return {
        "id": aluno.id,
        "turma_id": aluno.turma_id,
        "nome": aluno.nome,
        "empresa": aluno.empresa,
        "ra": aluno.ra,
        "chamada": aluno.chamada,
        "ativo": aluno.ativo,
        "criado_em": aluno.criado_em,
        "atualizado_em": aluno.atualizado_em,
        "turma": aluno.turma.nome_turma if aluno.turma else None,
        "cod_turma": aluno.turma.cod_turma if aluno.turma else None
    }


@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(dados: AlunoCreate, db: Session = Depends(get_db)):
    aluno = aluno_service.criar(db, dados)
    return {
        "id": aluno.id,
        "turma_id": aluno.turma_id,
        "nome": aluno.nome,
        "empresa": aluno.empresa,
        "ra": aluno.ra,
        "chamada": aluno.chamada,
        "ativo": aluno.ativo,
        "criado_em": aluno.criado_em,
        "atualizado_em": aluno.atualizado_em,
        "turma": aluno.turma.nome_turma if aluno.turma else None,
        "cod_turma": aluno.turma.cod_turma if aluno.turma else None
    }


@router.patch("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = aluno_service.atualizar(db, aluno_id, dados)
    return {
        "id": aluno.id,
        "turma_id": aluno.turma_id,
        "nome": aluno.nome,
        "empresa": aluno.empresa,
        "ra": aluno.ra,
        "chamada": aluno.chamada,
        "ativo": aluno.ativo,
        "criado_em": aluno.criado_em,
        "atualizado_em": aluno.atualizado_em,
        "turma": aluno.turma.nome_turma if aluno.turma else None,
        "cod_turma": aluno.turma.cod_turma if aluno.turma else None
    }


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def desativar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno_service.desativar(db, aluno_id)

@router.post("/import/batch")
def importar_alunos_lote(dados: list[AlunoImport], db: Session = Depends(get_db)):
    return aluno_service.importar_lote(db, dados)

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.aluno_service import AlunoService
from app.models.schemas import AlunoCreate, AlunoUpdate, AlunoResponse
from app.auth.permissions import exigir_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alunos", tags=["alunos"])


def get_aluno_service() -> AlunoService:
    return AlunoService()


@router.get("", response_model=list[AlunoResponse])
def listar_alunos(
    turma: str | None = Query(default=None),
    svc: AlunoService = Depends(get_aluno_service),
):
    if turma:
        return svc.listar_por_turma(turma)
    return svc.listar_todos()


@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(
    aluno_id: int,
    svc: AlunoService = Depends(get_aluno_service),
):
    try:
        return svc.buscar_por_id(aluno_id)
    except Exception:
        logger.exception("Erro ao buscar aluno %d", aluno_id)
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")


@router.post("", status_code=201, response_model=AlunoResponse,
             dependencies=[Depends(exigir_role("admin"))])
def criar_aluno(
    dados: AlunoCreate,
    svc: AlunoService = Depends(get_aluno_service),
):
    return svc.criar(dados.model_dump())


@router.patch("/{aluno_id}", status_code=204,
              dependencies=[Depends(exigir_role("admin"))])
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    svc: AlunoService = Depends(get_aluno_service),
):
    try:
        svc.atualizar(aluno_id, dados.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{aluno_id}", status_code=204,
               dependencies=[Depends(exigir_role("admin"))])
def deletar_aluno(
    aluno_id: int,
    svc: AlunoService = Depends(get_aluno_service),
):
    try:
        svc.deletar(aluno_id)
    except LookupError:
        logger.exception("Aluno %d não encontrado para deleção", aluno_id)
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

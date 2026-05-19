import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.services.aluno_service import AlunoService
from app.models.schemas import AlunoCreate, AlunoUpdate, AlunoResponse
from app.auth.permissions import exigir_role
from app.auth.token_validator import validar_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alunos", tags=["alunos"])


def get_aluno_service() -> AlunoService:
    return AlunoService()


@router.get("", response_model=list[AlunoResponse],
            dependencies=[Depends(validar_token)])
def listar_alunos(
    turma: str | None = Query(default=None),
    svc: AlunoService = Depends(get_aluno_service),
):
    if turma:
        return svc.listar_por_turma(turma)
    return svc.listar_todos()


@router.get("/{aluno_id}", response_model=AlunoResponse,
            dependencies=[Depends(validar_token)])
def buscar_aluno(
    aluno_id: int,
    svc: AlunoService = Depends(get_aluno_service),
):
    try:
        return svc.buscar_por_id(aluno_id)
    except LookupError:
        logger.exception("Aluno %d não encontrado", aluno_id)
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


class AlunoImportItem(BaseModel):
    nome: str
    turma: str | None = None
    cod_turma: str
    chamada: int | None = None
    termo: int | None = None


class ImportResponse(BaseModel):
    total: int
    sucesso: int
    erro: int
    detalhes: list[dict]


@router.post("/import/batch", status_code=200, response_model=ImportResponse,
             dependencies=[Depends(exigir_role("admin"))])
def importar_alunos_lote(
    dados: list[AlunoImportItem],
    svc: AlunoService = Depends(get_aluno_service),
):
    """Importar lista de alunos em lote"""
    resultado = {
        "total": len(dados),
        "sucesso": 0,
        "erro": 0,
        "detalhes": []
    }

    for item in dados:
        try:
            # Validação básica
            if not item.nome or not item.nome.strip():
                raise ValueError("Nome está vazio")
            if not item.cod_turma or not item.cod_turma.strip():
                raise ValueError("Código da turma está vazio")

            aluno_dict = {
                "nome": item.nome.strip(),
                "turma": (item.turma or item.cod_turma).strip(),
                "cod_turma": item.cod_turma.strip()
            }

            if item.chamada is not None:
                aluno_dict["chamada"] = item.chamada

            logger.info(f"Importando aluno: {aluno_dict}")
            svc.criar(aluno_dict)
            resultado["sucesso"] += 1
            resultado["detalhes"].append({
                "nome": item.nome,
                "status": "sucesso"
            })

        except Exception as e:
            resultado["erro"] += 1
            erro_msg = str(e)
            logger.exception(f"Erro ao importar aluno {item.nome}: {erro_msg}")
            resultado["detalhes"].append({
                "nome": item.nome,
                "status": "erro",
                "mensagem": erro_msg
            })

    return resultado

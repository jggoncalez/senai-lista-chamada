import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.chamada_service import ChamadaService
from app.models.schemas import ChamadaCreate, ChamadaUpdate, ChamadaResponse
from app.auth.permissions import exigir_role
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chamadas", tags=["chamadas"])


def get_chamada_service() -> ChamadaService:
    return ChamadaService()


@router.post("", status_code=201, response_model=ChamadaResponse,
             dependencies=[Depends(exigir_role("professor", "admin"))])
def registrar_chamada(
    chamada: ChamadaCreate,
    svc: ChamadaService = Depends(get_chamada_service),
):
    try:
        resultado = svc.registrar(chamada)
        return ChamadaResponse(id=resultado.get("ID"), presente=chamada.presente)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/relatorio",
            dependencies=[Depends(exigir_role("professor", "admin"))])
def relatorio(
    turma: str = Query(...),
    data: str = Query(...),
    svc: ChamadaService = Depends(get_chamada_service),
):
    return svc.relatorio(turma, data)


@router.patch("/{chamada_id}", status_code=204,
              dependencies=[Depends(exigir_role("professor", "admin"))])
def corrigir_presenca(
    chamada_id: int,
    dados: ChamadaUpdate,
    svc: ChamadaService = Depends(get_chamada_service),
):
    svc.atualizar_presenca(chamada_id, dados.presente)


@router.delete("/{chamada_id}", status_code=204,
               dependencies=[Depends(exigir_role("admin"))])
def deletar_chamada(
    chamada_id: int,
    svc: ChamadaService = Depends(get_chamada_service),
):
    try:
        svc.sp.deletar(settings.CHAMADAS_LIST_NAME, chamada_id)
    except Exception:
        logger.exception("Erro ao deletar chamada %d", chamada_id)
        raise HTTPException(status_code=404, detail="Chamada não encontrada.")

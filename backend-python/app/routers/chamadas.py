from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.presenca import (
    PresencaCreate,
    PresencaUpdate,
    PresencaResponse,
    ChamadaLoteCreate,
    ChamadaRelatorioResponse,
)
from app.services import chamada_service

router = APIRouter(prefix="/chamadas", tags=["chamadas"])


@router.post("/lote", response_model=list[PresencaResponse])
def registrar_lote(dados: ChamadaLoteCreate, db: Session = Depends(get_db)):
    return chamada_service.registrar_lote(db, dados.sessao_id, dados.presencas)


@router.get("/sessao/{sessao_id}", response_model=list[PresencaResponse])
def listar_por_sessao(sessao_id: int, db: Session = Depends(get_db)):
    return chamada_service.listar_por_sessao(db, sessao_id)


@router.post("/", response_model=PresencaResponse, status_code=status.HTTP_201_CREATED)
def registrar(dados: PresencaCreate, db: Session = Depends(get_db)):
    return chamada_service.registrar(db, dados)


@router.patch("/{presenca_id}", response_model=PresencaResponse)
def atualizar(presenca_id: int, dados: PresencaUpdate, db: Session = Depends(get_db)):
    return chamada_service.atualizar(db, presenca_id, dados)

@router.post("/relatorio-semanal", tags=["chamadas"])
def enviar_relatorio_semanal_manual(db: Session = Depends(get_db)):
    from app.services.email_service import enviar_relatorio_semanal
    enviar_relatorio_semanal(db)
    return {"status": "ok", "mensagem": "Relatórios enviados com sucesso"}

from fastapi import APIRouter, Depends
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
def get_me():
    # Retorno dummy para integração inicial
    return {
        "nome": "Professor Coordenador",
        "email": "coordenador@senai.br",
        "roles": ["admin", "professor"]
    }

from fastapi import APIRouter, Depends
from app.auth.token_validator import validar_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(usuario: dict = Depends(validar_token)):
    """
    Frontend chama isso logo que carrega pra saber
    o nome, email e role do professor logado.
    """
    return usuario
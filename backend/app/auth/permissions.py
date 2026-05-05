from fastapi import Depends, HTTPException
from app.auth.token_validator import validar_token


def exigir_role(*roles: str):
    """
    Uso nos routers:
        @router.post("", dependencies=[Depends(exigir_role("professor", "admin"))])
    """
    async def verificar(usuario: dict = Depends(validar_token)):
        roles_do_usuario = usuario.get("roles", [])
        if not any(r in roles_do_usuario for r in roles):
            raise HTTPException(
                status_code=403,
                detail=f"Acesso negado. Requer: {', '.join(roles)}."
            )
        return usuario
    return verificar
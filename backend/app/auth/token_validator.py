from fastapi import Header, HTTPException
from app.config import settings


async def validar_token(authorization: str = Header(default="")) -> dict:
    """
    Dev (DEBUG=true):  aceita qualquer requisição, retorna usuário fake.
    Prod (DEBUG=false): aqui entraria a validação real do JWT do Azure AD.
    """
    if settings.DEBUG:
        # Facilita muito o desenvolvimento — sem precisar de MSAL configurado
        return {
            "nome": "Professor Dev",
            "email": "dev@sesisenai.com.br",
            "roles": ["professor", "admin"],
        }

    # Produção: valida o Bearer token do Microsoft
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente.")

    # TODO: implementar quando tiver App Registration aprovado pela TI
    # token = authorization.removeprefix("Bearer ")
    # payload = _validar_jwt_azure(token)
    # return payload

    raise HTTPException(status_code=501, detail="Auth em produção ainda não implementado.")
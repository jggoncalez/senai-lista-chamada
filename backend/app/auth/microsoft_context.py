from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.auth.token_response import TokenResponse
from app.config import settings

def _device_code_callback(device_code_response: TokenResponse):
    """Exibe o código pro usuário no terminal."""
    print("\n─────────────────────────────────────")
    print("  Acesse: https://microsoft.com/devicelogin")
    print(f"  Código: {device_code_response.user_code}")
    print("─────────────────────────────────────\n")

def get_sharepoint_context() -> ClientContext:
    # Modo 1 — App Registration (produção)
    if settings.CLIENT_ID and settings.CLIENT_SECRET:
        return ClientContext(settings.SHAREPOINT_URL).with_credentials(
            ClientCredential(settings.CLIENT_ID, settings.CLIENT_SECRET)
        )

    # Modo 2 — Device Code Flow (dev com MFA)
    if settings.CLIENT_ID and not settings.CLIENT_SECRET:
        return ClientContext(settings.SHAREPOINT_URL).with_interactive(
            tenant=settings.TENANT_ID,
            client_id=settings.CLIENT_ID,
            callback=_device_code_callback
        )

    # Modo 3 — Usuário e senha (dev sem MFA)
    if settings.SP_USERNAME and settings.SP_PASSWORD:
        return ClientContext(settings.SHAREPOINT_URL).with_credentials(
            UserCredential(settings.SP_USERNAME, settings.SP_PASSWORD)
        )

    raise ValueError(
        "Nenhuma credencial configurada no .env"
    )
import threading

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
from app.config import settings

_context: ClientContext | None = None
_lock = threading.Lock()


def get_sharepoint_context() -> ClientContext:
    """Retorna sempre o mesmo ClientContext — autentica uma única vez por processo.
    Thread-safe via double-checked locking."""
    global _context
    if _context is not None:
        return _context

    with _lock:
        if _context is not None:
            return _context

        # Modo 1 — App Registration (produção)
        if settings.CLIENT_ID and settings.CLIENT_SECRET:
            _context = ClientContext(settings.SHAREPOINT_URL).with_credentials(
                ClientCredential(settings.CLIENT_ID, settings.CLIENT_SECRET)
            )

        # Modo 2 — Device Code Flow (dev com MFA, usa client público da Microsoft)
        elif settings.DEVICE_FLOW_TENANT:
            _context = ClientContext(settings.SHAREPOINT_URL).with_device_flow(
                tenant=settings.DEVICE_FLOW_TENANT,
                client_id=settings.DEVICE_FLOW_CLIENT_ID,
            )

        # Modo 3 — Usuário e senha (dev sem MFA)
        elif settings.SP_USERNAME and settings.SP_PASSWORD:
            _context = ClientContext(settings.SHAREPOINT_URL).with_credentials(
                UserCredential(settings.SP_USERNAME, settings.SP_PASSWORD)
            )

        else:
            raise ValueError("Nenhuma credencial configurada no .env")

    return _context

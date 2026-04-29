from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from app.config import settings

def get_sharepoint_context() -> ClientContext:
    credentials = ClientCredential(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET
        )
    return ClientContext(settings.SHAREPOINT_URL).with_credentials(credentials)
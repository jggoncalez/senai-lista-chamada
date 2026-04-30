import os
from pathlib import Path

from dotenv import load_dotenv

import pytest
from unittest.mock import MagicMock, patch

# Carrega o .env real ANTES de setar os defaults,
# para que o teste real use o SharePoint verdadeiro.
backend_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=backend_dir / ".env")

# Defaults para testes unitários (só entram se o .env não tiver o valor)
os.environ.setdefault("SHAREPOINT_URL", "https://fake.sharepoint.com/sites/test")
os.environ.setdefault("CLIENT_ID", "")
os.environ.setdefault("CLIENT_SECRET", "")
os.environ.setdefault("TENANT_ID", "")


@pytest.fixture
def mock_sp():
    """SharePointService mockado — sem conexão real ao SharePoint."""
    with patch("app.services.aluno_service.SharePointService") as MockSP, \
         patch("app.services.chamada_service.SharePointService") as MockSPChamada:

        sp_instance = MagicMock()
        MockSP.return_value = sp_instance
        MockSPChamada.return_value = sp_instance
        yield sp_instance

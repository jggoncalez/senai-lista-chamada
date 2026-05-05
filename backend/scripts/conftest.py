"""
Configuração para os scripts de integração em backend/scripts/.
Garante que o pacote `app` seja encontrado e que o .env correto seja carregado,
independentemente de onde o pytest for iniciado.
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
load_dotenv(dotenv_path=backend_dir / ".env")

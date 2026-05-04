"""
Script de diagnóstico de conexão com o SharePoint.

Como rodar (de qualquer diretório):
    python backend/scripts/teste_conexao.py

Ou direto do diretório backend/:
    python scripts/teste_conexao.py

Modo Device Flow: uma mensagem pedirá o código para autenticar em
    https://microsoft.com/devicelogin
"""
import sys
from pathlib import Path

# Garante que o pacote `app` seja encontrado independente de onde o script é chamado
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_dir / ".env")

from app.config import settings

print("=" * 60)
print("  Diagnóstico de Conexão — SharePoint")
print("=" * 60)
print(f"\nURL do site : {settings.SHAREPOINT_URL}")

if settings.CLIENT_ID and settings.CLIENT_SECRET:
    print("Modo de auth: App Registration (produção)")
elif settings.DEVICE_FLOW_TENANT:
    print(f"Modo de auth: Device Flow (tenant: {settings.DEVICE_FLOW_TENANT})")
    print(f"Client ID   : {settings.DEVICE_FLOW_CLIENT_ID}")
    print("\nVocê precisará abrir o navegador e acessar:")
    print("  https://microsoft.com/devicelogin")
    print("Depois insira o código que aparecer no terminal.\n")
elif settings.SP_USERNAME and settings.SP_PASSWORD:
    print(f"Modo de auth: Usuário/senha ({settings.SP_USERNAME})")
else:
    print("\n[ERRO] Nenhuma credencial configurada no .env!")
    print("Adicione DEVICE_FLOW_TENANT ou CLIENT_ID+CLIENT_SECRET.")
    sys.exit(1)

print("-" * 60)
print("Conectando...")

try:
    from office365.sharepoint.client_context import ClientContext
    from office365.runtime.auth.client_credential import ClientCredential
    from office365.runtime.auth.user_credential import UserCredential

    if settings.CLIENT_ID and settings.CLIENT_SECRET:
        ctx = ClientContext(settings.SHAREPOINT_URL).with_credentials(
            ClientCredential(settings.CLIENT_ID, settings.CLIENT_SECRET)
        )
    elif settings.DEVICE_FLOW_TENANT:
        ctx = ClientContext(settings.SHAREPOINT_URL).with_device_flow(
            settings.DEVICE_FLOW_TENANT,
            settings.DEVICE_FLOW_CLIENT_ID,
        )
    else:
        ctx = ClientContext(settings.SHAREPOINT_URL).with_credentials(
            UserCredential(settings.SP_USERNAME, settings.SP_PASSWORD)
        )

    web = ctx.web.get().execute_query()
    print(f"\n[OK] Conexão estabelecida!")
    print(f"  Site : {web.title}")
    print(f"  URL  : {web.url}")

    listas = ctx.web.lists.filter("Hidden eq false").get().execute_query()
    print(f"\nListas disponíveis ({len(listas)} encontradas):")
    for lista in listas:
        print(f"  → {lista.properties['Title']}")

except Exception as e:
    print(f"\n[ERRO] Falha na conexão: {e}")
    sys.exit(1)

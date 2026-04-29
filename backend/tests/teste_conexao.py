# backend/teste_conexao.py
from dotenv import load_dotenv
load_dotenv()

from office365.sharepoint.client_context import ClientContext
import os

SHAREPOINT_URL = os.getenv("SHAREPOINT_URL")

# Client ID público do SharePoint Online Management Shell (Microsoft)
# Não precisa criar App Registration — já está pré-autorizado na maioria dos tenants
PUBLIC_CLIENT_ID = "9bc3ab49-b65d-410a-85ad-de819febfddc"

# Extrai o tenant do domínio do SharePoint (ex: sesisenaispedu.onmicrosoft.com)
# ou use o domínio personalizado (ex: senaisp.edu.br)
TENANT = "sesisenaispedu.onmicrosoft.com"

print(f"Conectando em: {SHAREPOINT_URL}")
print("Sera aberto um prompt de autenticacao no terminal.\n")
print("Acesse https://microsoft.com/devicelogin e insira o codigo exibido.\n")

try:
    ctx = ClientContext(SHAREPOINT_URL).with_device_flow(TENANT, PUBLIC_CLIENT_ID)

    web = ctx.web.get().execute_query()
    print(f"\nConexao OK!")
    print(f"  Site: {web.title}")
    print(f"  URL:  {web.url}\n")

    listas = ctx.web.lists.get().execute_query()
    print("Listas encontradas:")
    for lista in listas:
        print(f"  -> {lista.properties['Title']}")

except Exception as e:
    print(f"\nErro: {e}")

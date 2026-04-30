# backend/tests/inspecionar_listas.py
from dotenv import load_dotenv
load_dotenv()

from office365.sharepoint.client_context import ClientContext
import os

SHAREPOINT_URL = os.getenv("SHAREPOINT_URL")
PUBLIC_CLIENT_ID = "9bc3ab49-b65d-410a-85ad-de819febfddc"
TENANT = "sesisenaispedu.onmicrosoft.com"

print("Acesse https://microsoft.com/devicelogin e insira o codigo exibido.\n")

ctx = ClientContext(SHAREPOINT_URL).with_device_flow(TENANT, PUBLIC_CLIENT_ID)

for nome_lista in ["lst_alunos", "lst_presenca_alunos"]:
    print(f"\nLista: {nome_lista}")
    print("-" * 40)

    items = (
        ctx.web.lists
        .get_by_title(nome_lista)
        .items.get()
        .execute_query()
    )

    if items:
        colunas = list(items[0].properties.keys())
        print(f"Total de colunas: {len(colunas)}")
        print("Colunas disponíveis:")
        for chave in colunas:
            print(f"  -> {chave}: {items[0].properties[chave]}")
    else:
        print("  Lista vazia — sem itens ainda")

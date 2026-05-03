# Dependências

#senai #chamada #dependencias #python #npm

> [[00 - Índice|← Índice]]

---

## Backend — `requirements.txt`

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
Office365-REST-Python-Client==2.6.2
httpx==0.27.0
python-jose[cryptography]==3.3.0
pydantic==2.8.0
pydantic-settings==2.4.0
python-dotenv==1.0.1
pytest==8.3.0
pytest-asyncio==0.24.0
```

### Instalação

```bash
cd backend
pip install -r requirements.txt
```

---

## Frontend — `package.json` (principais)

| Pacote | Versão | Uso |
|---|---|---|
| `@azure/msal-browser` | `^3.x` | Login Microsoft / MSAL.js |
| `xlsx` | `^0.18.x` | Parse de Excel para importação |

### Instalação

```bash
cd frontend
npm install
```

### Inicializar SvelteKit (primeira vez)

```bash
npm create svelte@latest .
```

---

## Links relacionados

- [[02 - Stack e Decisões Técnicas]] — por que cada lib foi escolhida
- [[06 - Autenticação]] — `Office365-REST-Python-Client` e `python-jose`
- [[10 - Import de Excel]] — pacote `xlsx`
- [[15 - Próximos Passos]] — migração futura para `msgraph-sdk`

# Variáveis de Ambiente

#senai #chamada #config #env #segurança

> [[00 - Índice|← Índice]]

---

## `backend-python/.env`

```bash
# ── Azure SQL Database ───────────────────────
DATABASE_URL=mssql+pymssql://usuario:senha@server.database.windows.net/lista-chamada
```

> **Formato:** `mssql+pymssql://user:pass@host/database`
> Não adicionar `?driver=...` — o `pymssql` não usa ODBC.

### `backend-python/.env.example`

```bash
DATABASE_URL=mssql+pymssql://usuario:senha@server.database.windows.net/db_chamadas
```

---

## `frontend/.env`

```bash
VITE_API_URL=http://localhost:8000
VITE_CLIENT_ID=xxxx-xxxx-xxxx
VITE_TENANT_ID=xxxx-xxxx-xxxx
VITE_REDIRECT_URI=http://localhost:5173/login
```

---

## Requisitos de sistema (não são variáveis de ambiente)

Para `pymssql` funcionar, o `FreeTDS` precisa estar instalado:

```bash
sudo pacman -S freetds    # Arch / CachyOS
# ou
sudo apt install freetds-dev  # Ubuntu / Debian
```

---

## Banco serverless (Azure SQL)

O Azure SQL no tier **serverless** entra em sleep após inatividade e retorna erro `40613` na primeira requisição.
O `connect_args={"login_timeout": 60}` no engine aguarda até 60s pelo wake-up automático.

---

## ⚠️ Segurança

- Nunca commitar `.env` com credenciais reais
- Usar `.env.example` para documentar as chaves sem valores
- Em produção, injetar via **GitHub Secrets** → ver [[12 - CI-CD]]

---

## Links relacionados

- [[07 - Backend FastAPI]] — `database.py` que lê `DATABASE_URL`
- [[05 - Schema Azure SQL]] — estrutura do banco
- [[11 - Hospedagem]] — configuração em produção no Azure

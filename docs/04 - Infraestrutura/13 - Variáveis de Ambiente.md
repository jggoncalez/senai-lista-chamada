# Variáveis de Ambiente

#senai #chamada #config #env #segurança

> [[00 - Índice|← Índice]]

---

## `backend/.env`

```bash
# ── SharePoint ──────────────────────────────
SHAREPOINT_URL=https://sesisenaispedu.sharepoint.com/sites/ProtoWebsite

# ── Modo desenvolvimento – usuário e senha ──
SP_USERNAME=seuemail@sesisenai.com.br
SP_PASSWORD=suasenha

# ── Modo desenvolvimento – Device Code Flow ─
# CLIENT_ID=xxxx-xxxx-xxxx
# TENANT_ID=xxxx-xxxx-xxxx

# ── Modo produção – App Registration ────────
# CLIENT_ID=xxxx-xxxx-xxxx
# CLIENT_SECRET=xxxx-xxxx-xxxx
# TENANT_ID=xxxx-xxxx-xxxx

# ── Nomes das listas ─────────────────────────
ALUNOS_LIST_NAME=lst_alunos
CHAMADAS_LIST_NAME=lst_presenca_alunos

# ── App ──────────────────────────────────────
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:5173"]
```

> A lógica de seleção do modo de auth baseada nessas variáveis está em [[06 - Autenticação]].

---

## `frontend/.env`

```bash
VITE_API_URL=http://localhost:8000
VITE_CLIENT_ID=xxxx-xxxx-xxxx
VITE_TENANT_ID=xxxx-xxxx-xxxx
VITE_REDIRECT_URI=http://localhost:5173/login
```

---

## Qual modo de auth é ativado?

| Variáveis presentes | Modo |
|---|---|
| `CLIENT_ID` + `CLIENT_SECRET` | App Registration (produção) |
| `CLIENT_ID` + `TENANT_ID` | Device Code Flow (dev com MFA) |
| `SP_USERNAME` + `SP_PASSWORD` | Usuário + senha (dev sem MFA) |

---

## ⚠️ Segurança

- Nunca commitar `.env` com credenciais reais
- Usar `.env.example` para documentar as chaves sem valores
- Em produção, injetar via **GitHub Secrets** → ver [[12 - CI-CD]]

---

## Links relacionados

- [[06 - Autenticação]] — como as variáveis determinam o modo de auth
- [[07 - Backend FastAPI]] — `config.py` que lê essas variáveis
- [[11 - Hospedagem]] — configuração em produção no Azure

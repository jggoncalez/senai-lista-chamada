# Backend — FastAPI

#senai #chamada #backend #fastapi #python

> [[00 - Índice|← Índice]]

---

## Camadas

```mermaid
graph LR
    R[Routers\nalunos.py\nchamadas.py\nauth.py] --> S[Services\naluno_service.py\nchamada_service.py]
    S --> SP[sharepoint_service.py\nCRUD genérico]
    SP --> C[microsoft_context.py\n→ ver [[06 - Autenticação]]]
```

---

## `config.py`

Usa `pydantic-settings` — lê do `.env` automaticamente.
Variáveis completas em [[13 - Variáveis de Ambiente]].

---

## `services/sharepoint_service.py` — CRUD genérico

Métodos disponíveis: `listar`, `buscar_por_id`, `criar`, `atualizar`, `deletar`.
Todos operam sobre qualquer lista passada como `nome_lista`.

---

## `services/aluno_service.py`

| Método | Descrição |
|---|---|
| `criar(dados)` | Cria aluno em `lst_alunos` |
| `listar_todos()` | Retorna todos os alunos |
| `listar_por_turma(turma)` | Filtra por `Cod_x002e_Turma` |
| `buscar_por_id(id)` | Busca aluno específico |
| `atualizar(id, dados)` | Atualiza campos fornecidos |
| `deletar(id)` | Verifica existência e deleta |

> Colunas do SharePoint → ver [[05 - SharePoint - Listas]]

---

## `services/chamada_service.py`

| Método | Descrição |
|---|---|
| `registrar(chamada)` | Cria registro, verifica duplicata |
| `listar_por_turma(cod_turma)` | Todos os registros da turma |
| `relatorio(cod_turma, data)` | Filtra por turma + data |
| `atualizar_presenca(id, presente)` | Corrige presença |
| `deletar(id)` | Remove registro |

---

## `utils/retry.py`

Retry com **backoff exponencial**: 2s → 4s → 8s (padrão: 3 tentativas).

---

## Endpoints

| Método | Endpoint              | Descrição                  | Role             |
| ------ | --------------------- | -------------------------- | ---------------- |
| GET    | `/auth/me`            | dados do usuário logado    | qualquer         |
| GET    | `/alunos`             | listar todos               | qualquer         |
| GET    | `/alunos?turma=3DEVT` | filtrar por turma          | qualquer         |
| POST   | `/alunos`             | criar aluno                | admin            |
| POST   | `/alunos/importar`    | importar lote              | admin            |
| PATCH  | `/alunos/{id}`        | atualizar aluno            | admin            |
| DELETE | `/alunos/{id}`        | deletar aluno              | admin            |
| POST   | `/chamadas`           | registrar chamada          | professor, admin |
| GET    | `/chamadas/relatorio` | relatório por turma e data | professor, admin |
| PATCH  | `/chamadas/{id}`      | corrigir presença          | professor, admin |
| DELETE | `/chamadas/{id}`      | deletar registro           | admin            |

---

## `models/schemas.py` — Schemas Pydantic

- `AlunoCreate` / `AlunoUpdate`
- `ChamadaCreate` / `ChamadaUpdate`
- `ImportResult` — resultado do import em lote

---

## Links relacionados

- [[05 - SharePoint - Listas]] — mapeamento das colunas
- [[06 - Autenticação]] — `microsoft_context.py` e roles
- [[13 - Variáveis de Ambiente]] — configuração do backend
- [[14 - Dependências]] — `requirements.txt`

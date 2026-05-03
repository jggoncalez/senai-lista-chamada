# Frontend — SvelteKit

#senai #chamada #frontend #sveltekit #typescript

> [[00 - Índice|← Índice]]

---

## `lib/api/client.ts` — fetch autenticado

Toda requisição ao backend usa `Bearer token` automaticamente:

```typescript
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
    const token = await getToken();
    return fetch(`${BASE}${path}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        }
    });
}
```

---

## Stores (`lib/stores/`)

### `chamada.ts`

| Store | Tipo | Uso |
|---|---|---|
| `registros` | `Map<number, RegistroChamada>` | alunos e seus estados de presença |
| `turmaSelecionada` | `string` | turma em andamento |
| `disciplina` | `string` | disciplina selecionada |
| `dataAula` | `string` | ISO date, default = hoje |

### `auth.ts`

Armazena o usuário logado (retorno do `/auth/me`).

---

## Lógica de chamada — padrão "marcar ausentes"

> Por padrão **todos os alunos começam como presentes**.
> Professor só desmarca quem **faltou**.

**Benefício:** Em turma de 30 alunos com 2 faltas → 2 cliques, não 28.

---

## `lib/auth/msal.ts`

Gerencia login/logout/getToken via **MSAL.js** (`@azure/msal-browser`).
Configuração via variáveis de ambiente → ver [[13 - Variáveis de Ambiente]].

---

## `lib/utils/excelParser.ts`

Parse inteligente de `.xlsx` e `.csv` com mapeamento automático de colunas.
Detalhes completos em [[10 - Import de Excel]].

---

## Links relacionados

- [[07 - Backend FastAPI]] — endpoints consumidos
- [[09 - Páginas do Sistema]] — rotas e componentes de cada página
- [[10 - Import de Excel]] — `excelParser.ts`
- [[13 - Variáveis de Ambiente]] — `VITE_*` do frontend
- [[14 - Dependências]] — `package.json`

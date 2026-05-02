# 📘 Guia Svelte — Projeto SENAI Lista de Chamada

> Guia prático baseado no backend real do projeto.
> O backend usa **FastAPI + Python** conectado ao **SharePoint** via `Office365-REST-Python-Client`.
> O frontend em Svelte vai consumir essa API e autenticar via **Device Flow da Microsoft**.

---

## Índice

1. [O que já existe no backend](#1-o-que-já-existe-no-backend)
2. [Setup do frontend Svelte](#2-setup-do-frontend-svelte)
3. [Estrutura de arquivos sugerida](#3-estrutura-de-arquivos-sugerida)
4. [Sintaxe básica do Svelte](#4-sintaxe-básica-do-svelte)
5. [Reatividade — o coração do Svelte](#5-reatividade--o-coração-do-svelte)
6. [Componentes e props](#6-componentes-e-props)
7. [Stores — estado global (usuário logado)](#7-stores--estado-global-usuário-logado)
8. [Roteamento com SvelteKit](#8-roteamento-com-sveltekit)
9. [Autenticação Microsoft (MSAL)](#9-autenticação-microsoft-msal)
10. [Proteção de rotas por tipo de usuário](#10-proteção-de-rotas-por-tipo-de-usuário)
11. [Consumindo a API do backend](#11-consumindo-a-api-do-backend)
12. [Tela de Alunos — consumindo `/alunos`](#12-tela-de-alunos--consumindo-alunos)
13. [Tabela de Presença — consumindo `/chamadas`](#13-tabela-de-presença--consumindo-chamadas)
14. [Tempo real com polling](#14-tempo-real-com-polling)
15. [Próximos passos](#15-próximos-passos)

---

## 1. O que já existe no backend

Antes de codar o frontend, entenda o que o backend já entrega:

### Modelos (schemas)

```python
# backend/app/models/schemas.py

class ChamadaCreate(BaseModel):
    nome_aluno: str
    cod_turma: str
    data_aula: str   # formato ISO: "2026-04-29"
    disciplina: str
    presente: bool

class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: str
    cod_turma: str
    chamada: int   # número de chamadas feitas
    termo: int
```

### Serviços já implementados

| Serviço | Métodos disponíveis |
|---|---|
| `AlunoService` | `listar_todos()`, `listar_por_turma(cod)`, `buscar_por_id(id)`, `criar(dados)`, `atualizar(id, dados)`, `deletar(id)` |
| `ChamadaService` | `registrar(chamada)`, `atualizar_presenca(id, presente)`, `relatorio(cod_turma, data)` |

### Configurações relevantes (`.env.example`)

```env
SHAREPOINT_URL=https://sesisenaispedu.sharepoint.com/sites/exemplo
DEVICE_FLOW_TENANT=sesisenaispedu.onmicrosoft.com
# Em produção:
# CLIENT_ID=xxxx
# CLIENT_SECRET=xxxx
# TENANT_ID=xxxx
```

O `ALLOWED_ORIGINS` no `config.py` já está com `http://localhost:5173` — que é exatamente a porta padrão do Svelte dev. ✅

### O que ainda está vazio (precisa implementar antes do frontend funcionar)

- `backend/app/main.py` — instanciar o FastAPI e registrar os routers
- `backend/app/routers/alunos.py` — rotas HTTP para `AlunoService`
- `backend/app/routers/chamadas.py` — rotas HTTP para `ChamadaService`
- `backend/app/routers/auth.py` — rota `/auth/tipo?email=...` que o frontend vai consumir
- `backend/app/auth/token_validator.py` — validar o token JWT da Microsoft

---

## 2. Setup do frontend Svelte

O projeto já tem a pasta `frontend/` com um `.gitkeep`. É lá que o SvelteKit vai morar.

```bash
# Na raiz do repositório
cd frontend
npx sv create .        # cria dentro da pasta frontend já existente
npm install
npm run dev            # roda em http://localhost:5173
```

Instale as dependências necessárias:

```bash
npm install @azure/msal-browser
```

---

## 3. Estrutura de arquivos sugerida

```
frontend/
├── src/
│   ├── routes/
│   │   ├── +layout.svelte          ← inicializa MSAL + navbar global
│   │   ├── +page.svelte            ← redireciona para /login ou /turmas
│   │   ├── login/
│   │   │   └── +page.svelte        ← tela de login Microsoft
│   │   ├── turmas/
│   │   │   ├── +layout.svelte      ← guard: só logado
│   │   │   ├── +page.svelte        ← lista de turmas do usuário
│   │   │   └── [cod]/
│   │   │       └── +page.svelte    ← presença da turma /turmas/DS01
│   │   └── admin/
│   │       ├── +layout.svelte      ← guard: só administrador
│   │       └── +page.svelte        ← painel admin (vincular turmas, gerenciar usuários)
│   ├── lib/
│   │   ├── components/
│   │   │   ├── CardTurma.svelte
│   │   │   ├── TabelaPresenca.svelte
│   │   │   └── Navbar.svelte
│   │   ├── stores/
│   │   │   └── auth.js             ← estado global do usuário
│   │   └── api.js                  ← todas as chamadas ao backend
│   └── app.html
└── package.json
```

---

## 4. Sintaxe básica do Svelte

Um arquivo `.svelte` tem 3 seções:

```svelte
<script>
  // Lógica JavaScript
  let nome = "João";
  let count = 0;

  function incrementar() {
    count++;
  }
</script>

<!-- Template HTML -->
<h1>Olá, {nome}!</h1>
<p>Contagem: {count}</p>
<button on:click={incrementar}>Clique aqui</button>

<style>
  /* CSS com escopo automático — não vaza para outros componentes */
  h1 { color: #c00; }
</style>
```

### Diretivas essenciais

```svelte
<script>
  let logado = true;
  let alunos = ["Ana", "Bruno", "Carlos"];
  let busca = "";
</script>

<!-- Condicional -->
{#if logado}
  <p>Bem-vindo!</p>
{:else}
  <a href="/login">Entrar</a>
{/if}

<!-- Loop — o (aluno) entre parênteses é a key, como no React -->
{#each alunos as aluno, i (aluno)}
  <li>{i + 1}. {aluno}</li>
{/each}

<!-- Binding bidirecional (two-way) -->
<input bind:value={busca} placeholder="Buscar aluno..." />
<p>Buscando: {busca}</p>
```

---

## 5. Reatividade — o coração do Svelte

### Declarações reativas com `$:`

```svelte
<script>
  // Exemplo real do projeto: calcular % de presença da turma
  let alunos = [
    { nome: "Ana", presente: true },
    { nome: "Bruno", presente: false },
    { nome: "Carlos", presente: true },
  ];

  // Recalcula automaticamente toda vez que "alunos" muda
  $: presentes = alunos.filter(a => a.presente).length;
  $: porcentagem = alunos.length > 0
    ? ((presentes / alunos.length) * 100).toFixed(1)
    : 0;

  // Bloco reativo — roda quando qualquer variável interna muda
  $: {
    if (Number(porcentagem) < 75) {
      console.warn("Turma com presença abaixo do mínimo!");
    }
  }
</script>

<p>{presentes}/{alunos.length} presentes — {porcentagem}%</p>
```

### Arrays — atenção!

```svelte
<script>
  let lista = [{ nome: "Ana", presente: false }];

  function marcarPresente(index) {
    // ✅ Correto — reatribuição dispara update na UI
    lista[index] = { ...lista[index], presente: true };
    lista = lista; // garante reatividade

    // ❌ Errado — mutação direta não atualiza a UI
    // lista[index].presente = true;
  }
</script>
```

---

## 6. Componentes e props

### `src/lib/components/CardTurma.svelte`

```svelte
<script>
  // Props declaradas com "export let"
  export let codTurma;      // ex: "DS01"
  export let nomeTurma;     // ex: "DS 3A"
  export let totalAlunos;
  export let presentes;
  export let onClick = () => {};

  $: porcentagem = totalAlunos > 0
    ? ((presentes / totalAlunos) * 100).toFixed(0)
    : 0;
</script>

<div class="card" on:click={onClick} role="button" tabindex="0">
  <span class="cod">{codTurma}</span>
  <h3>{nomeTurma}</h3>
  <p>{presentes}/{totalAlunos} presentes</p>
  <div class="barra">
    <div class="progresso" style="width: {porcentagem}%"></div>
  </div>
  <span class="pct">{porcentagem}%</span>
</div>

<style>
  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.25rem;
    cursor: pointer;
    transition: box-shadow 0.2s;
  }
  .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
  .cod { font-size: 0.75rem; color: #666; text-transform: uppercase; }
  .barra { background: #eee; border-radius: 4px; height: 6px; margin: 0.5rem 0; }
  .progresso { background: #d62828; height: 100%; border-radius: 4px; transition: width 0.3s; }
</style>
```

### Usando o componente em uma página

```svelte
<script>
  import CardTurma from "$lib/components/CardTurma.svelte";
  import { goto } from "$app/navigation";

  let turmas = [
    { cod: "DS01", nome: "DS 3A", total: 32, presentes: 28 },
    { cod: "RD02", nome: "RD 2B", total: 25, presentes: 20 },
  ];
</script>

<div class="grid">
  {#each turmas as t (t.cod)}
    <CardTurma
      codTurma={t.cod}
      nomeTurma={t.nome}
      totalAlunos={t.total}
      presentes={t.presentes}
      onClick={() => goto(`/turmas/${t.cod}`)}
    />
  {/each}
</div>
```

### Eventos de filho para pai

```svelte
<!-- Filho: BotaoPresenca.svelte -->
<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let nomeAluno;
  export let presente;
</script>

<button on:click={() => dispatch("toggle", { nomeAluno, novoValor: !presente })}>
  {presente ? "✅ Presente" : "❌ Ausente"}
</button>
```

```svelte
<!-- Pai recebe o evento com on:toggle -->
<BotaoPresenca
  nomeAluno="Ana"
  presente={true}
  on:toggle={(e) => console.log(e.detail.nomeAluno, e.detail.novoValor)}
/>
```

---

## 7. Stores — estado global (usuário logado)

### `src/lib/stores/auth.js`

```javascript
import { writable, derived } from "svelte/store";

// writable = pode ser lido e escrito de qualquer componente
export const usuario = writable(null);
// Formato esperado:
// { nome: "João", email: "joao@sesisenaispedu.org.br", tipo: "administrador" }

// derived = calculado a partir de outro store (como useMemo no React)
export const isAdmin = derived(
  usuario,
  ($usuario) => $usuario?.tipo === "administrador"
);

export const isLogado = derived(
  usuario,
  ($usuario) => $usuario !== null
);
```

### Usando em qualquer componente com o prefixo `$`

```svelte
<script>
  import { usuario, isAdmin, isLogado } from "$lib/stores/auth";
  // O $ assina o store automaticamente — sem useEffect, sem subscribe manual
</script>

{#if $isLogado}
  <p>Olá, {$usuario.nome}!</p>

  {#if $isAdmin}
    <a href="/admin">⚙️ Painel Admin</a>
  {:else}
    <a href="/turmas">📋 Minhas Turmas</a>
  {/if}
{:else}
  <a href="/login">Entrar</a>
{/if}
```

### Atualizando de qualquer arquivo

```javascript
import { usuario } from "$lib/stores/auth";

// Setar
usuario.set({ nome: "João", email: "joao@sesisenaispedu.org.br", tipo: "comum" });

// Limpar (logout)
usuario.set(null);
```

---

## 8. Roteamento com SvelteKit

Roteamento **baseado em arquivo** — sem configuração extra:

```
src/routes/
├── +page.svelte              → /
├── login/+page.svelte        → /login
├── turmas/+page.svelte       → /turmas
├── turmas/[cod]/+page.svelte → /turmas/DS01  (rota dinâmica)
└── admin/+page.svelte        → /admin
```

### Lendo o parâmetro dinâmico

```svelte
<!-- src/routes/turmas/[cod]/+page.svelte -->
<script>
  import { page } from "$app/stores";

  // $page.params.cod === "DS01" quando a URL for /turmas/DS01
  $: codTurma = $page.params.cod;
</script>

<h1>Turma: {codTurma}</h1>
```

### Navegação programática

```svelte
<script>
  import { goto } from "$app/navigation";
</script>

<button on:click={() => goto("/turmas/DS01")}>
  Ver turma DS01
</button>
```

### Carregando dados com `+page.js` (antes de renderizar)

```javascript
// src/routes/turmas/[cod]/+page.js
export async function load({ params, fetch }) {
  const res = await fetch(`http://localhost:8000/alunos/turma/${params.cod}`);
  const alunos = await res.json();
  return { alunos, cod: params.cod };
}
```

```svelte
<!-- src/routes/turmas/[cod]/+page.svelte -->
<script>
  export let data; // recebido automaticamente do load()
</script>

<h1>Turma {data.cod}</h1>
{#each data.alunos as aluno}
  <p>{aluno.nome}</p>
{/each}
```

---

## 9. Autenticação Microsoft (MSAL)

O backend já usa o **Device Flow** com o `CLIENT_ID` público da Microsoft (`9bc3ab49...`).
No frontend usamos o **Login Popup** do MSAL Browser — mesmo tenant, fluxo diferente.

### `src/lib/auth.js`

```javascript
import { PublicClientApplication } from "@azure/msal-browser";
import { usuario } from "$lib/stores/auth";

// Mesmo TENANT que está no .env do backend
const msalConfig = {
  auth: {
    clientId: "9bc3ab49-b65d-410a-85ad-de819febfddc", // client público da Microsoft
    authority: "https://login.microsoftonline.com/sesisenaispedu.onmicrosoft.com",
    redirectUri: "http://localhost:5173",
  },
};

let msalInstance;

export async function initMsal() {
  msalInstance = new PublicClientApplication(msalConfig);
  await msalInstance.initialize();

  // Tenta recuperar sessão já existente no browser
  const accounts = msalInstance.getAllAccounts();
  if (accounts.length > 0) {
    const conta = accounts[0];
    usuario.set({
      nome: conta.name,
      email: conta.username,
      tipo: await buscarTipoUsuario(conta.username),
    });
  }
}

export async function loginMicrosoft() {
  const result = await msalInstance.loginPopup({
    scopes: ["User.Read", "openid", "profile", "email"],
  });

  const conta = result.account;
  const tipo = await buscarTipoUsuario(conta.username);

  usuario.set({ nome: conta.name, email: conta.username, tipo });
  return tipo;
}

export async function logout() {
  await msalInstance.logoutPopup();
  usuario.set(null);
}

export async function getToken() {
  const accounts = msalInstance.getAllAccounts();
  if (!accounts.length) return null;

  const result = await msalInstance.acquireTokenSilent({
    scopes: ["User.Read"],
    account: accounts[0],
  });
  return result.accessToken;
}

// Consulta o backend para saber se é admin ou comum
async function buscarTipoUsuario(email) {
  try {
    const res = await fetch(`http://localhost:8000/auth/tipo?email=${email}`);
    const data = await res.json();
    return data.tipo; // "administrador" ou "comum"
  } catch {
    return "comum"; // fallback seguro
  }
}
```

### Layout raiz inicializa o MSAL: `src/routes/+layout.svelte`

```svelte
<script>
  import { onMount } from "svelte";
  import { initMsal } from "$lib/auth";

  onMount(async () => {
    await initMsal();
  });
</script>

<slot />
```

### Página de login: `src/routes/login/+page.svelte`

```svelte
<script>
  import { loginMicrosoft } from "$lib/auth";
  import { goto } from "$app/navigation";

  let carregando = false;
  let erro = "";

  async function handleLogin() {
    carregando = true;
    erro = "";
    try {
      const tipo = await loginMicrosoft();
      goto(tipo === "administrador" ? "/admin" : "/turmas");
    } catch (e) {
      erro = "Erro ao fazer login. Tente novamente.";
      console.error(e);
    } finally {
      carregando = false;
    }
  }
</script>

<div class="container">
  <h1>📋 Lista de Chamada</h1>
  <p>Entre com sua conta institucional SENAI</p>

  {#if erro}
    <p class="erro">{erro}</p>
  {/if}

  <button on:click={handleLogin} disabled={carregando}>
    {carregando ? "Entrando..." : "🏢 Entrar com Microsoft"}
  </button>
</div>
```

---

## 10. Proteção de rotas por tipo de usuário

### Guard para `/admin`: `src/routes/admin/+layout.svelte`

```svelte
<script>
  import { isLogado, isAdmin } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    if (!$isLogado) goto("/login");
    else if (!$isAdmin) goto("/turmas"); // usuário comum não entra aqui
  });
</script>

{#if $isAdmin}
  <slot />
{/if}
```

### Guard para `/turmas`: `src/routes/turmas/+layout.svelte`

```svelte
<script>
  import { isLogado } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    if (!$isLogado) goto("/login");
  });
</script>

{#if $isLogado}
  <slot />
{/if}
```

---

## 11. Consumindo a API do backend

### `src/lib/api.js` — camada centralizada de API

```javascript
import { getToken } from "$lib/auth";

const BASE = "http://localhost:8000";

async function authHeaders() {
  const token = await getToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// ── Alunos ──────────────────────────────────────────────────────────────────

export async function getAlunosPorTurma(codTurma) {
  const res = await fetch(`${BASE}/alunos/turma/${codTurma}`, {
    headers: await authHeaders(),
  });
  if (!res.ok) throw new Error("Erro ao buscar alunos");
  return res.json();
}

export async function getTodosAlunos() {
  const res = await fetch(`${BASE}/alunos`, {
    headers: await authHeaders(),
  });
  if (!res.ok) throw new Error("Erro ao buscar alunos");
  return res.json();
}

export async function criarAluno(dados) {
  // dados = { nome, turma, cod_turma }
  const res = await fetch(`${BASE}/alunos`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify(dados),
  });
  if (!res.ok) throw new Error("Erro ao criar aluno");
  return res.json();
}

export async function deletarAluno(id) {
  const res = await fetch(`${BASE}/alunos/${id}`, {
    method: "DELETE",
    headers: await authHeaders(),
  });
  if (!res.ok) throw new Error("Erro ao deletar aluno");
}

// ── Chamadas ─────────────────────────────────────────────────────────────────

export async function getRelatorio(codTurma, data) {
  // data no formato "2026-04-29"
  const res = await fetch(
    `${BASE}/chamadas/relatorio?cod_turma=${codTurma}&data=${data}`,
    { headers: await authHeaders() }
  );
  if (!res.ok) throw new Error("Erro ao buscar relatório");
  return res.json();
}

export async function registrarChamada(chamada) {
  // chamada = { nome_aluno, cod_turma, data_aula, disciplina, presente }
  // Corresponde ao schema ChamadaCreate do backend
  const res = await fetch(`${BASE}/chamadas`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify(chamada),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao registrar chamada");
  }
  return res.json();
}

export async function atualizarPresenca(itemId, presente) {
  const res = await fetch(`${BASE}/chamadas/${itemId}`, {
    method: "PATCH",
    headers: await authHeaders(),
    body: JSON.stringify({ presente }),
  });
  if (!res.ok) throw new Error("Erro ao atualizar presença");
}
```

---

## 12. Tela de Alunos — consumindo `/alunos`

```svelte
<!-- src/routes/turmas/[cod]/+page.svelte -->
<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { getAlunosPorTurma } from "$lib/api";
  import TabelaPresenca from "$lib/components/TabelaPresenca.svelte";

  $: codTurma = $page.params.cod;

  let alunos = [];
  let carregando = true;
  let erro = "";

  onMount(async () => {
    try {
      alunos = await getAlunosPorTurma(codTurma);
    } catch (e) {
      erro = e.message;
    } finally {
      carregando = false;
    }
  });
</script>

<h1>Turma {codTurma}</h1>

{#if carregando}
  <p>Carregando alunos...</p>
{:else if erro}
  <p class="erro">{erro}</p>
{:else if alunos.length === 0}
  <p>Nenhum aluno encontrado nesta turma.</p>
{:else}
  <TabelaPresenca {alunos} {codTurma} />
{/if}
```

---

## 13. Tabela de Presença — consumindo `/chamadas`

```svelte
<!-- src/lib/components/TabelaPresenca.svelte -->
<script>
  import { onMount } from "svelte";
  import { isAdmin } from "$lib/stores/auth";
  import { getRelatorio, registrarChamada, atualizarPresenca } from "$lib/api";

  export let alunos = [];   // lista de AlunoResponse do backend
  export let codTurma;

  let dataHoje = new Date().toISOString().split("T")[0]; // "2026-04-29"
  let disciplina = "";
  let registros = {};   // { nome_aluno: { id, presente } }
  let salvando = {};    // { nome_aluno: boolean } — loading por aluno

  onMount(async () => {
    await carregarRelatorio();
  });

  async function carregarRelatorio() {
    try {
      const chamadas = await getRelatorio(codTurma, dataHoje);
      registros = {};
      for (const c of chamadas) {
        registros[c.Nome_Aluno] = { id: c.ID, presente: c.Presente };
      }
    } catch (e) {
      console.error("Erro ao carregar relatório:", e);
    }
  }

  async function togglePresenca(aluno) {
    if (!$isAdmin) return; // usuário comum só visualiza

    salvando[aluno.nome] = true;
    const registroAtual = registros[aluno.nome];

    try {
      if (registroAtual) {
        // Registro já existe — atualiza
        await atualizarPresenca(registroAtual.id, !registroAtual.presente);
        registros[aluno.nome] = { ...registroAtual, presente: !registroAtual.presente };
      } else {
        // Novo registro — cria
        if (!disciplina) {
          alert("Informe a disciplina antes de registrar a chamada.");
          return;
        }
        const novo = await registrarChamada({
          nome_aluno: aluno.nome,
          cod_turma: codTurma,
          data_aula: dataHoje,
          disciplina,
          presente: true,
        });
        registros[aluno.nome] = { id: novo.ID, presente: true };
      }
      registros = registros; // força reatividade no objeto
    } catch (e) {
      alert(e.message);
    } finally {
      salvando[aluno.nome] = false;
    }
  }

  $: presentes = Object.values(registros).filter(r => r.presente).length;
  $: porcentagem = alunos.length > 0
    ? ((presentes / alunos.length) * 100).toFixed(1)
    : 0;
</script>

<div class="header">
  <div class="resumo">
    <strong>{presentes}/{alunos.length}</strong> presentes
    <span class="pct">{porcentagem}%</span>
  </div>

  {#if $isAdmin}
    <input
      bind:value={disciplina}
      placeholder="Disciplina (ex: Python)"
    />
    <input type="date" bind:value={dataHoje} />
  {/if}
</div>

<table>
  <thead>
    <tr>
      <th>#</th><th>Nome</th><th>Turma</th><th>Presença</th>
    </tr>
  </thead>
  <tbody>
    {#each alunos as aluno, i (aluno.id)}
      {@const reg = registros[aluno.nome]}
      <tr class:presente={reg?.presente} class:ausente={reg && !reg.presente}>
        <td>{i + 1}</td>
        <td>{aluno.nome}</td>
        <td>{aluno.turma}</td>
        <td>
          {#if $isAdmin}
            <button
              on:click={() => togglePresenca(aluno)}
              disabled={salvando[aluno.nome]}
            >
              {salvando[aluno.nome] ? "..." : (reg?.presente ? "✅ Presente" : "❌ Ausente")}
            </button>
          {:else}
            <span>{reg?.presente ? "✅" : reg ? "❌" : "—"}</span>
          {/if}
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  tr.presente { background: #f0fdf4; }
  tr.ausente  { background: #fff1f2; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 0.75rem 1rem; border-bottom: 1px solid #e5e7eb; text-align: left; }
  .header { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
</style>
```

---

## 14. Tempo real com polling

O backend conecta ao SharePoint — WebSockets seriam complexos de implementar lá.
A solução mais simples é **polling**: buscar o relatório a cada X segundos.

```svelte
<script>
  import { onMount, onDestroy } from "svelte";
  import { getRelatorio } from "$lib/api";

  export let codTurma;

  let registros = {};
  let intervalo;

  async function atualizar() {
    const data = new Date().toISOString().split("T")[0];
    try {
      const chamadas = await getRelatorio(codTurma, data);
      registros = {};
      for (const c of chamadas) {
        registros[c.Nome_Aluno] = { id: c.ID, presente: c.Presente };
      }
    } catch (e) {
      console.error("Polling falhou:", e);
    }
  }

  onMount(() => {
    atualizar();                              // carrega imediatamente
    intervalo = setInterval(atualizar, 10_000); // atualiza a cada 10s
  });

  onDestroy(() => {
    clearInterval(intervalo); // ⚠️ MUITO IMPORTANTE — limpa ao sair da página
  });
</script>
```

---

## 15. Próximos passos

### Checklist do frontend

- [ ] Criar o projeto em `frontend/` com `npx sv create .`
- [ ] Instalar `@azure/msal-browser`
- [ ] Criar `src/lib/stores/auth.js` (usuario, isAdmin, isLogado)
- [ ] Criar `src/lib/auth.js` (initMsal, loginMicrosoft, logout, getToken)
- [ ] Criar `src/lib/api.js` (getAlunosPorTurma, getRelatorio, registrarChamada, etc.)
- [ ] Layout raiz `+layout.svelte` com `initMsal()` no `onMount`
- [ ] Página `/login` com botão Microsoft
- [ ] Guards de rota nos layouts de `/turmas` e `/admin`
- [ ] Componente `TabelaPresenca.svelte` com lógica admin vs comum
- [ ] Polling de 10s para atualização em tempo real

### Checklist do backend (antes do frontend funcionar)

- [ ] `main.py` — instanciar FastAPI, registrar routers, configurar CORS
- [ ] `routers/alunos.py` — expor os métodos do `AlunoService` como endpoints HTTP
- [ ] `routers/chamadas.py` — expor os métodos do `ChamadaService` como endpoints HTTP
- [ ] `routers/auth.py` — endpoint `GET /auth/tipo?email=...` para o frontend consultar
- [ ] `auth/token_validator.py` — validar o JWT da Microsoft nas requests

### Recursos

| Recurso | Link |
|---|---|
| Documentação Svelte | https://svelte.dev/docs |
| Tutorial interativo | https://learn.svelte.dev |
| SvelteKit docs | https://kit.svelte.dev/docs |
| MSAL Browser | https://github.com/AzureAD/microsoft-authentication-library-for-js |

---

*Guia gerado com base no código real do repositório `senai-lista-chamada`*
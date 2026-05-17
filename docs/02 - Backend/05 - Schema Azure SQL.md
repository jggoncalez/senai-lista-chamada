# Schema Azure SQL

#senai #chamada #banco #sql #schema

> [[00 - Índice|← Índice]]

Banco: **Azure SQL Database** (`lista-chamada` em `senai.database.windows.net`)
ORM: **SQLAlchemy 2.x** via `pymssql` + `FreeTDS`

---

## Diagrama de entidades

```
cursos ──────────────────────────────┐
  │                                  │
  ├──── turma (curso_id)             │
  │       │                          │
  │       ├──── alunos (turma_id)    │
  │       │         │                │
  │       │         └── aluno_disciplina_extra (aluno_id, curso_id)
  │       │
  │       └──── turma_disciplina (turma_id, curso_id, professor_id)
  │                     │
  │                     └──── sessao_aula (turma_disciplina_id)
  │                                   │
  │                                   └──── presenca_alunos (sessao_id, aluno_id)
  │
usuarios ── roles (role_id)
  │
  └── turma_disciplina (professor_id)
  └── sessao_aula (professor_id)
```

---

## Tabelas

### `roles`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `nome` | NVARCHAR(50) UNIQUE | `'diretor'`, `'coordenador'`, `'professor'`, `'monitor'` |

---

### `usuarios`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `azure_object_id` | NVARCHAR(100) | nullable, preenchido após integrar MSAL |
| `nome` | NVARCHAR(200) | — |
| `email` | NVARCHAR(200) UNIQUE | — |
| `role_id` | INT FK → roles | — |
| `ativo` | BIT DEFAULT 1 | soft delete |
| `criado_em` | DATETIME2 | `GETDATE()` |

---

### `cursos`

> Representa uma disciplina com carga horária e eixo tecnológico.

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `nome` | NVARCHAR(200) | ex: `"Programação Orientada a Objetos"` |
| `carga_horaria` | INT | total de horas da disciplina |
| `eixo_tecnologico` | NVARCHAR(200) | nullable |
| `duracao_termos` | INT | número de termos em que é ministrada |
| `ativo` | BIT DEFAULT 1 | soft delete |
| `criado_em` | DATETIME2 | — |

---

### `turma`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `cod_turma` | NVARCHAR(50) UNIQUE | ex: `"3DEVT"` |
| `nome_turma` | NVARCHAR(200) | — |
| `curso_id` | INT FK → cursos | curso principal da turma |
| `termo` | INT | semestre atual (1–6) |
| `ativo` | BIT DEFAULT 1 | soft delete |
| `criado_em` / `atualizado_em` | DATETIME2 | — |

---

### `alunos`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `turma_id` | INT FK → turma | turma principal |
| `nome` | NVARCHAR(200) | — |
| `empresa` | NVARCHAR(100) | nullable (aprendiz) |
| `ra` | NVARCHAR(50) UNIQUE | registro acadêmico, nullable |
| `ativo` | BIT DEFAULT 1 | soft delete |
| `criado_em` / `atualizado_em` | DATETIME2 | — |

**Índice:** `idx_alunos_turma ON alunos(turma_id)`

---

### `turma_disciplina`

> Vínculo entre turma, disciplina (curso) e professor responsável, com o dia da semana.

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `turma_id` | INT FK → turma | — |
| `curso_id` | INT FK → cursos | a disciplina |
| `professor_id` | INT FK → usuarios | nullable |
| `dia_semana` | TINYINT | 0=Seg … 6=Dom (Python `weekday()`) |
| `ativo` | BIT DEFAULT 1 | soft delete |

**Constraint:** `UNIQUE (turma_id, curso_id, dia_semana)`
**Índice:** `idx_turma_disciplina ON turma_disciplina(turma_id)`

---

### `aluno_disciplina_extra`

> Aluno cursando uma disciplina fora da sua turma principal.

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `aluno_id` | INT FK → alunos | — |
| `curso_id` | INT FK → cursos | disciplina extra |
| `turma_id` | INT FK → turma | turma onde assiste, nullable |
| `ativo` | BIT DEFAULT 1 | — |

**Constraint:** `UNIQUE (aluno_id, curso_id)`

---

### `sessao_aula`

> Representa o momento real de uma chamada: turma + disciplina + data.

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `turma_disciplina_id` | INT FK → turma_disciplina | — |
| `professor_id` | INT FK → usuarios | quem abriu a chamada |
| `data_aula` | DATE | — |
| `observacao` | NVARCHAR(500) | nullable |
| `registrado_em` | DATETIME2 | `GETDATE()` |

**Constraint:** `UNIQUE (turma_disciplina_id, data_aula)` — uma sessão por disciplina por dia
**Índices:** `idx_sessao_data`, `idx_sessao_turma_disc`

---

### `presenca_alunos`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT IDENTITY PK | — |
| `sessao_id` | INT FK → sessao_aula | — |
| `aluno_id` | INT FK → alunos | — |
| `presente` | BIT | `1` = presente, `0` = falta |
| `observacao` | NVARCHAR(500) | nullable |

**Constraint:** `UNIQUE (sessao_id, aluno_id)` — um registro por aluno por sessão
**Índices:** `idx_presenca_sessao`, `idx_presenca_aluno`

---

## Links relacionados

- [[07 - Backend FastAPI]] — ORM models e services que mapeiam este schema
- [[13 - Variáveis de Ambiente]] — `DATABASE_URL`
- [[14 - Dependências]] — `pymssql`, `SQLAlchemy`

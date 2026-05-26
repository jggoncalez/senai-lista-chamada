# Estrutura de Pastas

#senai #chamada #estrutura

> [[00 - Índice|← Índice]]

---

```
senai-lista-chamada/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD → ver [[12 - CI-CD]]
│
├── backend-python/                 # Backend ativo (FastAPI + Azure SQL)
│   ├── app/
│   │   ├── models/                 # SQLAlchemy ORM
│   │   │   ├── __init__.py         # importa todos os models
│   │   │   ├── role.py             # Role
│   │   │   ├── usuario.py          # Usuario
│   │   │   ├── curso.py            # Curso (disciplina)
│   │   │   ├── turma.py            # Turma
│   │   │   ├── aluno.py            # Aluno
│   │   │   ├── turma_disciplina.py # TurmaDisciplina
│   │   │   ├── aluno_disciplina_extra.py
│   │   │   ├── sessao_aula.py      # SessaoAula
│   │   │   └── presenca.py         # PresencaAluno
│   │   ├── schemas/                # Pydantic v2
│   │   │   ├── curso.py
│   │   │   ├── turma.py
│   │   │   ├── aluno.py
│   │   │   ├── usuario.py
│   │   │   ├── turma_disciplina.py
│   │   │   ├── sessao_aula.py      # inclui AlunosSessaoResponse
│   │   │   └── presenca.py         # inclui ChamadaLoteCreate
│   │   ├── services/               # Lógica de negócio
│   │   │   ├── curso_service.py
│   │   │   ├── turma_service.py
│   │   │   ├── aluno_service.py
│   │   │   ├── usuario_service.py
│   │   │   ├── turma_disciplina_service.py
│   │   │   ├── sessao_aula_service.py
│   │   │   └── chamada_service.py  # registrar_lote (upsert)
│   │   ├── routers/                # Endpoints FastAPI
│   │   │   ├── cursos.py           # /cursos
│   │   │   ├── turmas.py           # /turmas
│   │   │   ├── alunos.py           # /alunos
│   │   │   ├── usuarios.py         # /usuarios
│   │   │   ├── turma_disciplinas.py # /turma-disciplinas
│   │   │   ├── sessoes.py          # /sessoes
│   │   │   └── chamadas.py         # /chamadas
│   │   ├── database.py             # engine, SessionLocal, get_db()
│   │   └── main.py                 # app FastAPI + CORS + routers
│   ├── .env                        # DATABASE_URL (não commitar)
│   ├── .env.example                # template
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── lib/
│       │   ├── auth/
│       │   │   ├── msal.ts             # login/logout/getToken
│       │   │   └── guard.ts            # proteção de rotas
│       │   ├── api/
│       │   │   ├── client.ts           # fetch base com Bearer token
│       │   │   ├── cursos.ts
│       │   │   ├── turmas.ts
│       │   │   ├── alunos.ts
│       │   │   ├── sessoes.ts
│       │   │   └── chamadas.ts
│       │   ├── stores/
│       │   │   ├── auth.ts
│       │   │   └── chamada.ts
│       │   ├── components/
│       │   │   ├── chamada/
│       │   │   │   ├── AlunoRow.svelte
│       │   │   │   └── ChamadaForm.svelte
│       │   │   └── ui/
│       │   │       └── Button.svelte
│       │   ├── types/
│       │   │   └── index.ts            # Aluno, Sessao, Presenca, Usuario
│       │   └── utils/
│       │       └── excelParser.ts
│       └── routes/
│           ├── login/
│           ├── chamada/
│           ├── relatorio/
│           └── importar/
│
├── docs/                           # este vault Obsidian
├── README.md
└── .gitignore
```

> **Nota:** a pasta `backend/` (SharePoint) ainda existe no repositório mas está obsoleta. O backend ativo é `backend-python/`.

---

## Links relacionados

- [[07 - Backend FastAPI]] — detalhes dos services e routers
- [[05 - Schema Azure SQL]] — tabelas mapeadas nos models
- [[08 - Frontend SvelteKit]] — stores, client e componentes

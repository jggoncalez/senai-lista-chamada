# Estrutura de Pastas

#senai #chamada #estrutura

> [[00 - Índice|← Índice]]

---

```
sistema-chamada/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD automático → ver [[12 - CI-CD]]
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── microsoft_context.py    # contexto SharePoint
│   │   │   ├── token_validator.py      # valida JWT do usuário logado
│   │   │   └── permissions.py          # controle por role (professor/admin)
│   │   ├── routers/
│   │   │   ├── auth.py                 # GET /auth/me
│   │   │   ├── alunos.py               # GET /alunos, POST /alunos
│   │   │   └── chamadas.py             # POST /chamadas, GET /chamadas/relatorio
│   │   ├── services/
│   │   │   ├── sharepoint_service.py   # CRUD genérico SharePoint
│   │   │   ├── aluno_service.py        # regras de negócio de alunos
│   │   │   └── chamada_service.py      # regras de negócio de chamadas
│   │   ├── models/
│   │   │   └── schemas.py              # schemas Pydantic
│   │   ├── utils/
│   │   │   └── retry.py                # retry com backoff exponencial
│   │   ├── middleware/
│   │   │   └── logging.py              # log de requisições
│   │   ├── main.py                     # app FastAPI + routers + CORS
│   │   └── config.py                   # Settings (pydantic-settings)
│   ├── tests/
│   │   ├── unit/
│   │   │   └── test_aluno_service.py
│   │   └── integration/
│   │       └── test_chamadas_router.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── lib/
│       │   ├── auth/
│       │   │   ├── msal.ts             # login/logout/getToken (MSAL.js)
│       │   │   └── guard.ts            # proteção de rotas
│       │   ├── api/
│       │   │   ├── client.ts           # fetch base com Bearer token automático
│       │   │   ├── alunos.ts           # fetchAlunos()
│       │   │   ├── chamadas.ts         # registrarChamada(), fetchRelatorio()
│       │   │   └── auth.ts             # fetchMe()
│       │   ├── stores/
│       │   │   ├── auth.ts             # usuário logado
│       │   │   └── chamada.ts          # estado da chamada em andamento
│       │   ├── components/
│       │   │   ├── chamada/
│       │   │   │   ├── AlunoRow.svelte
│       │   │   │   └── ChamadaForm.svelte
│       │   │   └── ui/
│       │   │       └── Button.svelte
│       │   ├── types/
│       │   │   └── index.ts            # Aluno, ChamadaPayload, Usuario
│       │   └── utils/
│       │       └── excelParser.ts      # parse inteligente de Excel/CSV
│       └── routes/
│           ├── login/
│           ├── chamada/
│           ├── relatorio/
│           └── importar/
├── docs/                               # este vault Obsidian
├── README.md
└── .gitignore
```

---

## Links relacionados

- [[07 - Backend FastAPI]] — detalhes dos services e routers
- [[08 - Frontend SvelteKit]] — stores, client e componentes
- [[06 - Autenticação]] — `auth/microsoft_context.py`

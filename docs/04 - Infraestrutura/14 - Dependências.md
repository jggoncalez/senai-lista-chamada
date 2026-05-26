# Dependências

#senai #chamada #dependencias #python #npm

> [[00 - Índice|← Índice]]

---

## Backend — `backend-python/requirements.txt`

```
fastapi
uvicorn[standard]
sqlalchemy
pymssql
python-dotenv
```

### Instalação

```bash
# 1. dependência de sistema (FreeTDS para pymssql)
sudo pacman -S freetds       # Arch / CachyOS
# ou: sudo apt install freetds-dev

# 2. dependências Python
cd backend-python
pip install -r requirements.txt
```

### Rodar o servidor

```bash
cd backend-python
uvicorn app.main:app --reload
# acesse http://localhost:8000/docs
```

---

## Por que `pymssql` em vez de `pyodbc`?

| | `pyodbc` | `pymssql` |
|---|---|---|
| Dependência de sistema | `unixodbc` + `msodbcsql18` (AUR) | `freetds` (pacman) |
| Instalação no Linux | Complexa (driver Microsoft via AUR) | Simples (`pacman`) |
| Licença adicional | Sim (Microsoft EULA) | Não |
| Suporte Azure SQL | Sim | Sim |

> `pyodbc` continua listado como alternativa se o ODBC Driver 18 for instalado. O formato da URL muda:
> `mssql+pyodbc://...?driver=ODBC+Driver+18+for+SQL+Server`

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
- [[13 - Variáveis de Ambiente]] — configuração do `DATABASE_URL`
- [[10 - Import de Excel]] — pacote `xlsx`

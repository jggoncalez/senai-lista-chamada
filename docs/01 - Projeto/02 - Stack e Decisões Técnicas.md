# Stack e Decisões Técnicas

#senai #chamada #stack #decisoes

> [[00 - Índice|← Índice]]

---

## Python + FastAPI

- Professor já conhece Python
- FastAPI é async, tipado, gera documentação automática em `/docs`
- SQLAlchemy ORM reduz SQL manual e garante segurança contra injeção
- Ecossistema Python forte para scripting e automações futuras

## SvelteKit

- Leve, sem overhead de Virtual DOM
- Compilado → bundle pequeno
- TypeScript nativo
- Stores reativos simples

---

## Por que NÃO Ruby on Rails?

- Sem suporte MSAL oficial
- Exigiria aprender Ruby do zero
- OAuth teria que ser implementado manualmente

## Por que NÃO C#/.NET?

- Seria a melhor escolha técnica (mesmo ecossistema Microsoft)
- Professor não conhece — deixado como **meta de longo prazo**

---

## Banco de dados: Azure SQL Database

Migração do SharePoint para um banco relacional dedicado.

| Aspecto | SharePoint (anterior) | Azure SQL (atual) |
|---|---|---|
| Consultas | CAML queries | SQL via SQLAlchemy ORM |
| Relacionamentos | Manual, via campos de texto | FK reais com integridade referencial |
| Performance | Lento (REST + SharePoint overhead) | Direto, pool de conexões |
| Schema | Colunas com nomes codificados (`Cod_x002e_Turma`) | Nomes limpos e tipados |
| Soft delete | Não suportado nativamente | `ativo BIT DEFAULT 1` |
| Auth necessária | Microsoft 365 + Office365-REST | String de conexão Azure SQL |

### Driver de conexão: `pymssql` + `FreeTDS`

Escolhido em vez de `pyodbc` por não exigir instalação do driver ODBC da Microsoft (que requer AUR no Arch/CachyOS).

```bash
sudo pacman -S freetds   # dependência de sistema
pip install pymssql      # driver Python
```

Formato da `DATABASE_URL`:
```
mssql+pymssql://usuario:senha@server.database.windows.net/database
```

---

## Biblioteca de ORM: `SQLAlchemy 2.x`

| Prós | Contras |
|---|---|
| ORM declarativo, sem SQL manual | Curva de aprendizado inicial |
| Pool de conexões embutido | Migrações requerem Alembic (futuro) |
| `pool_pre_ping` para Azure SQL serverless | — |
| Suporte a transactions + rollback automático | — |

---

## Links relacionados

- [[03 - Arquitetura]] — como a stack se integra
- [[05 - Schema Azure SQL]] — tabelas e relacionamentos
- [[14 - Dependências]] — versões exatas

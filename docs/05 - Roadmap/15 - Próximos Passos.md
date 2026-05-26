# Próximos Passos

#senai #chamada #backlog #roadmap

> [[00 - Índice|← Índice]]

---

## Concluído

- [x] Schema Azure SQL definido e documentado → [[05 - Schema Azure SQL]]
- [x] Conexão Azure SQL via `pymssql` + `FreeTDS` funcionando
- [x] Models SQLAlchemy ORM (9 tabelas com relationships)
- [x] Schemas Pydantic v2 (Base / Create / Update / Response)
- [x] Services CRUD completos com soft delete e rollback
- [x] 7 routers FastAPI com `response_model` tipado
- [x] Fluxo completo de chamada via `/sessoes` + `/chamadas/lote`
- [x] Endpoint `/turma-disciplinas/hoje` (filtro automático por dia)
- [x] `GET /sessoes/{id}/alunos` retorna turma + alunos extra
- [x] `POST /chamadas/lote` com upsert (pode reenviar sem duplicata)

---

## Imediato

- [ ] Popular o banco com dados reais (turmas, cursos, alunos, professores)
- [ ] Testar fluxo completo via `/docs` com dados reais
- [ ] Montar tela de chamada no SvelteKit → [[09 - Páginas do Sistema]]
- [ ] Implementar import de Excel para alunos → [[10 - Import de Excel]]

---

## Curto prazo

- [ ] Montar tela de login com MSAL.js
- [ ] Conectar frontend ao backend (client Svelte + stores)
- [ ] Montar relatório de presença
- [ ] Validar constraint `uq_sessao` no banco (uma sessão por dia por disciplina)

---

## Médio prazo

- [ ] Solicitar **App Registration** para a TI do SENAI → [[06 - Autenticação]]
- [ ] Integrar `azure_object_id` dos professores (vincular login MSAL ao `usuarios`)
- [ ] Deploy no Azure App Service + Static Web Apps → [[11 - Hospedagem]]
- [ ] Adicionar **Alembic** para gerenciar migrações de schema
- [ ] Testes automatizados com banco de teste isolado

---

## Longo prazo

- [ ] Exportação de relatórios em PDF/Excel
- [ ] Notificações por email para alunos com muitas faltas
- [ ] Dashboard de presença por turma/curso para coordenadores
- [ ] Migrar backend para **C#/.NET** → ver [[02 - Stack e Decisões Técnicas]]

---

## Links relacionados

- [[00 - Índice]] — status geral do projeto
- [[07 - Backend FastAPI]] — endpoints disponíveis
- [[06 - Autenticação]] — App Registration e MSAL
- [[11 - Hospedagem]] — deploy Azure

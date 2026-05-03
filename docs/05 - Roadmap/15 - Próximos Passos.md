# Próximos Passos

#senai #chamada #backlog #roadmap

> [[00 - Índice|← Índice]]

---

## Imediatos

- [ ] Instalar dependências do backend (`pip install -r requirements.txt`)
- [ ] Inicializar SvelteKit no frontend (`npm create svelte@latest .`)
- [ ] Testar endpoints do FastAPI com dados reais do SharePoint

---

## Curto prazo

- [ ] Montar tela de login com MSAL.js → [[09 - Páginas do Sistema]]
- [ ] Montar tela de chamada com lista de alunos
- [ ] Implementar import de Excel → [[10 - Import de Excel]]
- [ ] Montar relatório de presença

---

## Médio prazo

- [ ] Solicitar **App Registration** para a TI do SENAI → [[06 - Autenticação]]
- [ ] Migrar autenticação para MSAL (frontend) + JWT (backend)
- [ ] Deploy no Azure App Service + Static Web Apps → [[11 - Hospedagem]]
- [ ] Testes automatizados (pytest + pytest-asyncio) → [[14 - Dependências]]

---

## Longo prazo

- [ ] Migrar backend para **C#/.NET** (melhor integração Microsoft) → ver [[02 - Stack e Decisões Técnicas]]
- [ ] Migrar biblioteca SharePoint para **`msgraph-sdk`** (oficial, async)
- [ ] Exportação de relatórios em PDF/Excel
- [ ] Notificações por email para alunos com muitas faltas

---

## Links relacionados

- [[00 - Índice]] — status geral do projeto
- [[06 - Autenticação]] — App Registration e MSAL
- [[11 - Hospedagem]] — deploy Azure
- [[02 - Stack e Decisões Técnicas]] — decisões de longo prazo

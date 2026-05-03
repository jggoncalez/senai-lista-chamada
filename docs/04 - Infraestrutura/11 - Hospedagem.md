# Hospedagem

#senai #chamada #deploy #azure #infraestrutura

> [[00 - Índice|← Índice]]

---

## Estratégia principal — Azure (já contratado)

Reaproveitamento do Azure incluído no Microsoft 365 do SENAI.

| Serviço | Uso | Custo |
|---|---|---|
| Azure App Service F1 | Backend FastAPI | Gratuito (60min CPU/dia) |
| Azure Static Web Apps | Frontend SvelteKit | Gratuito |
| SharePoint Online | Banco de dados | Já pago |
| Azure Active Directory | Login Microsoft | Já pago |

> Se F1 for insuficiente → plano **B1** (~R$60/mês) elimina restrições.

---

## Alternativas gratuitas

Caso o Azure não seja liberado pela TI:

| Serviço | Backend | Frontend |
|---|---|---|
| Railway | ✅ 500h/mês | — |
| Render | ✅ dorme após 15min | — |
| Fly.io | ✅ 3 VMs grátis | — |
| Azure Static Web Apps | — | ✅ grátis |

---

## Deploy automático

O CI/CD via GitHub Actions faz deploy a cada push na `main`.
Detalhes completos em [[12 - CI-CD]].

---

## Links relacionados

- [[12 - CI-CD]] — pipeline de deploy
- [[13 - Variáveis de Ambiente]] — secrets necessários no GitHub
- [[15 - Próximos Passos]] — solicitar App Registration à TI

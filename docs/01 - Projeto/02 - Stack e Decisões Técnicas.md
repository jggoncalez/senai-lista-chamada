# Stack e Decisões Técnicas

#senai #chamada #stack #decisoes

> [[00 - Índice|← Índice]]

---

## Python + FastAPI

- Professor já conhece Python
- `Office365-REST-Python-Client` tem suporte nativo para SharePoint
- FastAPI é async, tipado, gera documentação automática em `/docs`
- Ecossistema Python forte

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
- Professor não conhece — deixado como **meta de médio prazo**

---

## Biblioteca SharePoint: `Office365-REST-Python-Client`

| Prós | Contras |
|---|---|
| Alto nível, abstrai URLs e auth | Síncrona (sem async nativo) |
| CRUD sem montar requests na mão | Sem suporte MSAL oficial |
| Comunidade ativa | — |
| Sem vulnerabilidades (verificado Snyk) | — |

> **Alternativa futura:** `msgraph-sdk` — oficial Microsoft, async → ver [[15 - Próximos Passos]]

---

## Links relacionados

- [[03 - Arquitetura]] — como a stack se integra
- [[14 - Dependências]] — versões exatas
- [[06 - Autenticação]] — limitações da biblioteca atual

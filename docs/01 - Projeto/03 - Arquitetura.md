# Arquitetura

#senai #chamada #arquitetura #diagrama

> [[00 - Índice|← Índice]]

---

## Visão de componentes

```mermaid
graph TD
    A[Navegador\nSvelteKit] -->|HTTPS + Bearer Token| B[Backend\nFastAPI]
    B -->|Office365-REST-Python-Client| C[Microsoft Graph\nSharePoint API]
    C --> D[(SharePoint Lists\nSENAI)]
    E[Azure Active Directory] -->|JWT| A
    A -->|login popup| E
```

---

## Fluxo de autenticação — Produção (planejado)

```mermaid
sequenceDiagram
    actor U as Usuário
    participant F as SvelteKit
    participant AAD as Azure AD (MSAL)
    participant B as FastAPI
    participant SP as SharePoint

    U->>F: Clica "Entrar com Microsoft"
    F->>AAD: Abre popup (MFA incluso)
    AAD-->>F: Retorna JWT token
    F->>B: Request com Authorization: Bearer <token>
    B->>AAD: Valida token (JWKS)
    B->>SP: Usa token para acessar listas
    SP-->>B: Dados
    B-->>F: Resposta JSON
```

---

## Fluxo atual — Desenvolvimento

```mermaid
flowchart LR
    A{Tem CLIENT_SECRET?} -->|Sim| B[App Registration\nclient_id + secret]
    A -->|Não| C{Tem TENANT_ID?}
    C -->|Sim| D[Device Code Flow\nusuário abre link no browser]
    C -->|Não| E[UserCredential\nusuário + senha\n⚠️ não usar em produção]
```

> A lógica de seleção está em [[06 - Autenticação]] → `microsoft_context.py`

---

## Links relacionados

- [[06 - Autenticação]] — implementação dos modos de auth
- [[07 - Backend FastAPI]] — serviços e endpoints
- [[08 - Frontend SvelteKit]] — cliente API e stores
- [[11 - Hospedagem]] — onde cada peça roda

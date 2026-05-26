---
tags:
  - senai
  - chamada
  - indice
---

# Sistema de Chamada — Índice

Projeto de controle de presença para o **SENAI Limeira**.
Stack: `Python/FastAPI` + `SQLAlchemy` + `Azure SQL Database` + `SvelteKit`

---

## 📁 01 - Projeto

| Nota | Conteúdo |
| --- | --- |
| [[01 - Visão Geral]] | Objetivo, contexto e público |
| [[02 - Stack e Decisões Técnicas]] | Por que cada tecnologia foi escolhida |
| [[03 - Arquitetura]] | Diagrama de componentes e fluxos |
| [[04 - Estrutura de Pastas]] | Organização do repositório |

## 📁 02 - Backend

| Nota | Conteúdo |
| --- | --- |
| [[05 - Schema Azure SQL]] | Tabelas, colunas e relacionamentos do banco |
| [[06 - Autenticação]] | Modos de auth e implementação |
| [[07 - Backend FastAPI]] | Models, schemas, services, endpoints |

## 📁 03 - Frontend

| Nota | Conteúdo |
| --- | --- |
| [[08 - Frontend SvelteKit]] | Stores, API client, componentes |
| [[09 - Páginas do Sistema]] | Rotas, roles e fluxo do professor |
| [[10 - Import de Excel]] | Fluxo de importação em 4 etapas |

## 📁 04 - Infraestrutura

| Nota | Conteúdo |
| --- | --- |
| [[11 - Hospedagem]] | Azure e alternativas gratuitas |
| [[12 - CI-CD]] | Pipeline GitHub Actions |
| [[13 - Variáveis de Ambiente]] | `.env` backend e frontend |
| [[14 - Dependências]] | `requirements.txt` e `package.json` |

## 📁 05 - Roadmap

| Nota | Conteúdo |
| --- | --- |
| [[15 - Próximos Passos]] | Backlog por prazo |

---

## Status Rápido

| Etapa | Status |
| --- | --- |
| Definição de stack | ✅ Concluído |
| Schema Azure SQL definido | ✅ Concluído |
| Conexão Azure SQL testada | ✅ Funcionando (pymssql + FreeTDS) |
| Models SQLAlchemy ORM | ✅ Concluído |
| Schemas Pydantic v2 | ✅ Concluído |
| Services com CRUD | ✅ Concluído |
| Routers FastAPI (7) | ✅ Concluído |
| Fluxo completo de chamada | ✅ Implementado |
| Frontend SvelteKit | ⏳ Pendente |
| Autenticação MSAL | ⏳ Pendente (aguarda App Registration) |
| Import Excel | ⏳ Pendente |
| Deploy | ⏳ Pendente |

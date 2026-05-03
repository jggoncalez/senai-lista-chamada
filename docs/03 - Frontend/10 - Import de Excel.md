# Import de Excel

#senai #chamada #excel #import #admin

> [[00 - Índice|← Índice]]

---

## Fluxo em 4 etapas

```mermaid
flowchart LR
    A["1️⃣ Upload\ndrag and drop\n.xlsx ou .csv"] --> B["2️⃣ Mapeamento\ndetecta colunas\nautomaticamente"]
    B --> C["3️⃣ Validação\ndestaca erros\nlinha a linha"]
    C --> D["4️⃣ Importar\nlote + barra\nde progresso"]
    D --> E[Relatório final\nimportados / falhas]
```

---

## Mapeamento inteligente de colunas

O parser (`lib/utils/excelParser.ts`) detecta variações de nome automaticamente:

| Nome no Excel | Campo do sistema |
|---|---|
| `Nome`, `Nome Completo`, `Aluno`, `Nome_Aluno` | `nome` |
| `Turma` | `turma` |
| `Cod.Turma`, `Cod_Turma`, `Codigo` | `cod_turma` |
| `Chamada`, `N.Chamada`, `Numero` | `chamada` |
| `Termo`, `Semestre` | `termo` |

---

## Validações aplicadas

- Nome vazio
- Código de turma vazio
- Número de chamada inválido (não numérico)
- Termo fora do intervalo 1–6

---

## Dependência necessária

```bash
npm install xlsx
```

> Ver [[14 - Dependências]] para versão exata.

---

## Endpoint de importação

`POST /alunos/importar` — role: `admin`
Retorna `ImportResult`: `{ importados: number, falhas: [{ linha, motivo }] }`

---

## Links relacionados

- [[09 - Páginas do Sistema]] — página `/importar`
- [[05 - SharePoint - Listas]] — estrutura de `lst_alunos`
- [[07 - Backend FastAPI]] — endpoint e schema `ImportResult`

# SharePoint — Listas

#senai #chamada #sharepoint #dados

> [[00 - Índice|← Índice]]

**URL do site:** `https://sesisenaispedu.sharepoint.com/sites/ProtoWebsite`

---

## Lista: `lst_alunos`

| Coluna SharePoint | Tipo | Observação |
|---|---|---|
| `Nome_Aluno` | Single line of text | nome completo |
| `Cod_x002e_Turma` | Single line of text | `Cod.Turma` codificado pelo SP |
| `Turma` | Single line of text | nome completo da turma |
| `Chamada` | Number | número de chamada |
| `Termo` | Number | semestre (1–6) |
| `ID` | Number | gerado pelo SharePoint |

> ⚠️ **Atenção:** O ponto em `Cod.Turma` é codificado como `_x002e_` pelo SharePoint.
> Usar **sempre** `Cod_x002e_Turma` no código.

**Turmas encontradas:** `3DEVT`, `2ADM`, `1DEVT`, `3ELET`

---

## Lista: `lst_presenca_alunos`

| Coluna SharePoint | Tipo | Observação |
|---|---|---|
| `Nome_Aluno` | Single line of text | nome do aluno |
| `Cod_x002e_Turma` | Single line of text | código da turma |
| `Data_Aula` | Date and Time | formato ISO com timezone |
| `Disciplina` | Single line of text | ex: `POO - Programação Orientada a Objetos` |
| `Presente` | Yes/No | `True` ou `False` |
| `ID` | Number | gerado pelo SharePoint |

---

## Links relacionados

- [[07 - Backend FastAPI]] — `sharepoint_service.py`, `aluno_service.py`, `chamada_service.py`
- [[06 - Autenticação]] — como o backend se conecta ao SharePoint
- [[10 - Import de Excel]] — importação em lote para `lst_alunos`

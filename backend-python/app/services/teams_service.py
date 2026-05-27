import httpx
import os
from google import genai  # type: ignore

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def _gerar_resumo_ia(
    turma: str,
    disciplina: str,
    data: str,
    total: int,
    presentes: int,
    alunos_risco: list[dict]
) -> str:
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Resumo indisponível — chave da IA não configurada."

    ausentes = total - presentes
    pct_geral = (presentes / total * 100) if total > 0 else 0

    nomes_risco = ", ".join(
        f"{a['nome']} ({a['pct']:.1f}%)"
        for a in alunos_risco
    ) or "nenhum"

    prompt = f"""Você é um assistente educacional do SENAI.
                Gere um parágrafo curto e profissional resumindo a chamada abaixo.
                Seja direto, sem introduções. Máximo 3 frases.

                Dados:
                - Turma: {turma}
                - Disciplina: {disciplina}
                - Data: {data}
                - Total de alunos: {total}
                - Presentes: {presentes}
                - Ausentes: {ausentes}
                - Frequência geral: {pct_geral:.1f}%
                - Alunos abaixo de 75%: {nomes_risco}
            """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception:
        return "Resumo indisponível — erro ao contatar IA."


def _build_adaptive_card(
    turma: str,
    disciplina: str,
    data: str,
    total: int,
    presentes: int,
    ausentes: int,
    pct_geral: float,
    alunos_risco: list[dict],
    resumo_ia: str,
) -> dict:
    freq_color = "Good" if pct_geral >= 75 else "Attention"

    header = {
        "type": "Container",
        "style": "emphasis",
        "bleed": True,
        "items": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "✅ Chamada Registrada",
                                "weight": "Bolder",
                                "size": "Large",
                            },
                            {
                                "type": "TextBlock",
                                "text": "SENAI — Sistema de Frequência",
                                "isSubtle": True,
                                "spacing": "None",
                            },
                        ],
                    }
                ],
            }
        ],
    }

    info_aula = {
        "type": "FactSet",
        "spacing": "Medium",
        "facts": [
            {"title": "Turma", "value": turma},
            {"title": "Disciplina", "value": disciplina},
            {"title": "Data", "value": data},
        ],
    }

    def _stat_column(label: str, value: str, style: str) -> dict:
        return {
            "type": "Column",
            "width": "stretch",
            "style": style,
            "items": [
                {
                    "type": "TextBlock",
                    "text": value,
                    "weight": "Bolder",
                    "size": "ExtraLarge",
                    "horizontalAlignment": "Center",
                },
                {
                    "type": "TextBlock",
                    "text": label,
                    "isSubtle": True,
                    "size": "Small",
                    "horizontalAlignment": "Center",
                    "spacing": "None",
                },
            ],
        }

    ausentes_style = "Attention" if ausentes > 0 else "Good"

    stats = {
    "type": "ColumnSet",
    "spacing": "Medium",
    "columns": [
        {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "TextBlock",
                    "text": f"👥 {total}",
                    "weight": "Bolder",
                    "size": "Large",
                    "horizontalAlignment": "Center",
                },
                {
                    "type": "TextBlock",
                    "text": "Total",
                    "isSubtle": True,
                    "size": "Small",
                    "horizontalAlignment": "Center",
                    "spacing": "None",
                },
            ],
        },
        {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "TextBlock",
                    "text": f"✅ {presentes}",
                    "weight": "Bolder",
                    "size": "Large",
                    "color": "Good",
                    "horizontalAlignment": "Center",
                },
                {
                    "type": "TextBlock",
                    "text": "Presentes",
                    "isSubtle": True,
                    "size": "Small",
                    "horizontalAlignment": "Center",
                    "spacing": "None",
                },
            ],
        },
        {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "TextBlock",
                    "text": f"❌ {ausentes}",
                    "weight": "Bolder",
                    "size": "Large",
                    "color": "Attention",
                    "horizontalAlignment": "Center",
                },
                {
                    "type": "TextBlock",
                    "text": "Ausentes",
                    "isSubtle": True,
                    "size": "Small",
                    "horizontalAlignment": "Center",
                    "spacing": "None",
                },
            ],
        },
        {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "TextBlock",
                    "text": f"📊 {pct_geral:.1f}%",
                    "weight": "Bolder",
                    "size": "Large",
                    "color": freq_color,
                    "horizontalAlignment": "Center",
                },
                {
                    "type": "TextBlock",
                    "text": "Frequência",
                    "isSubtle": True,
                    "size": "Small",
                    "horizontalAlignment": "Center",
                    "spacing": "None",
                },
            ],
        },
    ],
}

    body: list[dict] = [header, info_aula, stats]

    if alunos_risco:
        risco_header = {
            "type": "TextBlock",
            "text": "⚠️ Alunos com frequência abaixo de 75%",
            "weight": "Bolder",
            "color": "Attention",
            "spacing": "Medium",
        }

        table_header = {
            "type": "ColumnSet",
            "spacing": "Small",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [{"type": "TextBlock", "text": "**Aluno**", "weight": "Bolder", "size": "Small"}],
                },
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [{"type": "TextBlock", "text": "**Frequência**", "weight": "Bolder", "size": "Small", "horizontalAlignment": "Right"}],
                },
            ],
        }

        rows = []
        for aluno in alunos_risco:
            pct = aluno["pct"]
            badge_color = "Attention" if pct < 50 else "Warning"
            rows.append({
                "type": "ColumnSet",
                "spacing": "None",
                "separator": True,
                "columns": [
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [{"type": "TextBlock", "text": aluno["nome"], "size": "Small", "wrap": True}],
                    },
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": f"{pct:.1f}%",
                                "color": badge_color,
                                "weight": "Bolder",
                                "size": "Small",
                                "horizontalAlignment": "Right",
                            }
                        ],
                    },
                ],
            })

        body += [risco_header, table_header, *rows]
    else:
        body.append({
            "type": "TextBlock",
            "text": "✅ Todos os alunos estão com frequência regular.",
            "color": "Good",
            "spacing": "Medium",
            "isSubtle": True,
        })

    ia_container = {
        "type": "Container",
        "style": "accent",
        "spacing": "Medium",
        "items": [
            {
                "type": "TextBlock",
                "text": "🤖 Análise IA",
                "weight": "Bolder",
                "size": "Small",
            },
            {
                "type": "TextBlock",
                "text": resumo_ia,
                "wrap": True,
                "size": "Small",
                "spacing": "Small",
            },
        ],
    }
    body.append(ia_container)

    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": body,
    }

    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card,
            }
        ],
    }


def notificar_chamada(
    turma: str,
    disciplina: str,
    data: str,
    total: int,
    presentes: int,
    alunos_risco: list[dict]
):
    webhook_url = TEAMS_WEBHOOK_URL or os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        return

    ausentes = total - presentes
    pct_geral = (presentes / total * 100) if total > 0 else 0

    resumo_ia = _gerar_resumo_ia(
        turma, disciplina, data,
        total, presentes, alunos_risco
    )

    payload = _build_adaptive_card(
        turma=turma,
        disciplina=disciplina,
        data=data,
        total=total,
        presentes=presentes,
        ausentes=ausentes,
        pct_geral=pct_geral,
        alunos_risco=alunos_risco,
        resumo_ia=resumo_ia,
    )

    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(TEAMS_WEBHOOK_URL, json=payload)
    except Exception:
        pass

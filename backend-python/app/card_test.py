# backend-python/test_card.py
import json
from app.services.teams_service import _build_adaptive_card

card = _build_adaptive_card(
    turma="3DEVT",
    disciplina="Programação Orientada a Objetos",
    data="2026-05-27",
    total=8,
    presentes=5,
    ausentes=3,
    pct_geral=62.5,
    alunos_risco=[
        {"nome": "Nicolas Barbosa", "pct": 62.5},
        {"nome": "Pedro Henrique",  "pct": 58.3},
        {"nome": "Samuel Torres",   "pct": 70.1},
    ],
    resumo_ia="Na aula de Programação Orientada a Objetos da turma 3DEVT, registrou-se frequência de 62,5%, com 3 alunos ausentes. Nicolas Barbosa, Pedro Henrique e Samuel Torres encontram-se abaixo do limite mínimo de 75%, exigindo atenção imediata."
)

print(json.dumps(card, ensure_ascii=False, indent=2))
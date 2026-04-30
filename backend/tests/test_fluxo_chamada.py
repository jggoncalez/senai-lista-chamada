"""
Teste de fluxo: cria um aluno mockado e registra chamada para ele.
"""
import pytest
from app.services.aluno_service import AlunoService
from app.services.chamada_service import ChamadaService
from app.models.schemas import ChamadaCreate


ALUNO_RAW = {
    "ID": 1,
    "Nome_Aluno": "João Teste",
    "Turma": "DS-01",
    "Cod_x002e_Turma": "DS01",
    "Chamada": 0,
    "Termo": 1,
}


def test_criar_aluno_e_registrar_chamada(mock_sp):
    # ── 1. Cria o aluno ──────────────────────────────────────────────────────
    mock_sp.criar.return_value = ALUNO_RAW

    aluno_service = AlunoService()
    aluno = aluno_service.criar({
        "nome":      "João Teste",
        "turma":     "DS-01",
        "cod_turma": "DS01",
    })

    assert aluno["id"]   == 1
    assert aluno["nome"] == "João Teste"
    assert aluno["turma"] == "DS-01"

    # ── 2. Registra chamada para o aluno criado ───────────────────────────────
    mock_sp.listar.return_value = []  # nenhuma chamada existente
    mock_sp.criar.return_value = {
        "ID": 10,
        "Nome_Aluno": aluno["nome"],
        "Cod_x002e_Turma": aluno["cod_turma"],
        "Data_Aula": "2026-04-29",
        "Disciplina": "Python",
        "Presente": True,
    }

    chamada_service = ChamadaService()
    chamada = chamada_service.registrar(ChamadaCreate(
        nome_aluno=aluno["nome"],
        cod_turma=aluno["cod_turma"],
        data_aula="2026-04-29",
        disciplina="Python",
        presente=True,
    ))

    assert chamada["ID"] == 10
    assert chamada["Nome_Aluno"] == "João Teste"
    assert chamada["Presente"] is True
    mock_sp.criar.assert_called()


def test_nao_registra_chamada_duplicada_para_aluno(mock_sp):
    # Aluno já tem chamada registrada neste dia/disciplina
    mock_sp.listar.return_value = [{
        "Nome_Aluno": "João Teste",
        "Data_Aula":  "2026-04-29",
        "Disciplina": "Python",
    }]

    chamada_service = ChamadaService()

    with pytest.raises(ValueError, match="já registrada"):
        chamada_service.registrar(ChamadaCreate(
            nome_aluno="João Teste",
            cod_turma="DS01",
            data_aula="2026-04-29",
            disciplina="Python",
            presente=True,
        ))

    mock_sp.criar.assert_not_called()

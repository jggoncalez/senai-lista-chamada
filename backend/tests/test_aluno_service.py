import pytest
from app.services.aluno_service import AlunoService


ALUNOS_RAW = [
    {"ID": 1, "Nome_Aluno": "Ana Silva",   "Turma": "DS-01", "Cod_x002e_Turma": "DS01", "Chamada": 10, "Termo": 1},
    {"ID": 2, "Nome_Aluno": "Bruno Lima",  "Turma": "DS-01", "Cod_x002e_Turma": "DS01", "Chamada": 8,  "Termo": 1},
    {"ID": 3, "Nome_Aluno": "Carlos Melo", "Turma": "TI-02", "Cod_x002e_Turma": "TI02", "Chamada": 12, "Termo": 2},
]


def test_listar_todos_retorna_todos_alunos(mock_sp):
    mock_sp.listar.return_value = ALUNOS_RAW
    service = AlunoService()

    resultado = service.listar_todos()

    assert len(resultado) == 3
    assert resultado[0]["nome"] == "Ana Silva"
    assert resultado[2]["nome"] == "Carlos Melo"


def test_listar_todos_formata_campos(mock_sp):
    mock_sp.listar.return_value = ALUNOS_RAW
    service = AlunoService()

    aluno = service.listar_todos()[0]

    assert aluno["id"] == 1
    assert aluno["nome"] == "Ana Silva"
    assert aluno["turma"] == "DS-01"
    assert aluno["cod_turma"] == "DS01"
    assert aluno["chamada"] == 10
    assert aluno["termo"] == 1


def test_listar_por_turma_filtra_corretamente(mock_sp):
    # Mock simula retorno do SharePoint após filtro CAML por turma DS01
    mock_sp.listar.return_value = [ALUNOS_RAW[0], ALUNOS_RAW[1]]
    service = AlunoService()

    resultado = service.listar_por_turma("DS01")

    assert len(resultado) == 2
    assert all(a["cod_turma"] == "DS01" for a in resultado)


def test_listar_por_turma_inexistente_retorna_vazio(mock_sp):
    # Mock simula CAML sem resultados para turma inexistente
    mock_sp.listar.return_value = []
    service = AlunoService()

    resultado = service.listar_por_turma("TURMA_INEXISTENTE")

    assert resultado == []


def test_listar_todos_lista_vazia(mock_sp):
    mock_sp.listar.return_value = []
    service = AlunoService()

    resultado = service.listar_todos()

    assert resultado == []

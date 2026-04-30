import pytest
from app.services.chamada_service import ChamadaService
from app.models.schemas import ChamadaCreate


CHAMADA_BASE = ChamadaCreate(
    nome_aluno="Ana Silva",
    cod_turma="DS01",
    data_aula="2026-04-29",
    disciplina="Python",
    presente=True,
)

CHAMADAS_RAW = [
    {
        "Nome_Aluno": "Ana Silva",
        "Cod_x002e_Turma": "DS01",
        "Data_Aula": "2026-04-29T00:00:00",
        "Disciplina": "Python",
        "Presente": True,
    },
    {
        "Nome_Aluno": "Bruno Lima",
        "Cod_x002e_Turma": "DS01",
        "Data_Aula": "2026-04-29T00:00:00",
        "Disciplina": "Python",
        "Presente": False,
    },
    {
        "Nome_Aluno": "Carlos Melo",
        "Cod_x002e_Turma": "TI02",
        "Data_Aula": "2026-04-28T00:00:00",
        "Disciplina": "Redes",
        "Presente": True,
    },
]


def test_registrar_chamada_nova(mock_sp):
    mock_sp.listar.return_value = []
    mock_sp.criar.return_value = {"ID": 10, "Nome_Aluno": "Ana Silva"}
    service = ChamadaService()

    resultado = service.registrar(CHAMADA_BASE)

    assert resultado["ID"] == 10
    mock_sp.criar.assert_called_once()


def test_registrar_chamada_duplicada_levanta_erro(mock_sp):
    mock_sp.listar.return_value = [
        {
            "Nome_Aluno": "Ana Silva",
            "Data_Aula": "2026-04-29",
            "Disciplina": "Python",
        }
    ]
    service = ChamadaService()

    with pytest.raises(ValueError, match="já registrada"):
        service.registrar(CHAMADA_BASE)

    mock_sp.criar.assert_not_called()


def test_relatorio_filtra_por_turma_e_data(mock_sp):
    mock_sp.listar.return_value = CHAMADAS_RAW
    service = ChamadaService()

    resultado = service.relatorio("DS01", "2026-04-29")

    assert len(resultado) == 2
    assert all(c["Cod_x002e_Turma"] == "DS01" for c in resultado)


def test_relatorio_sem_resultados(mock_sp):
    mock_sp.listar.return_value = CHAMADAS_RAW
    service = ChamadaService()

    resultado = service.relatorio("DS01", "2099-01-01")

    assert resultado == []


def test_relatorio_filtra_por_turma_diferente(mock_sp):
    mock_sp.listar.return_value = CHAMADAS_RAW
    service = ChamadaService()

    resultado = service.relatorio("TI02", "2026-04-28")

    assert len(resultado) == 1
    assert resultado[0]["Nome_Aluno"] == "Carlos Melo"

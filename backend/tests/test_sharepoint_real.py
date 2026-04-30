"""
Teste de integração REAL contra o SharePoint.
Autentica via Device Flow — exige interação no navegador na 1ª execução.

Para rodar:
    pytest backend/tests/test_sharepoint_real.py -v -s
"""
import pytest
from dotenv import load_dotenv

from app.config import settings
from app.services.aluno_service import AlunoService
from app.services.chamada_service import ChamadaService
from app.models.schemas import ChamadaCreate

load_dotenv()

DATA_AULA = "2026-04-29"
DISCIPLINA = "Teste-Integração"
COD_TURMA  = "TESTE01"

ALUNOS_PARA_CRIAR = [
    {"nome": "Aluno Teste 1", "turma": "TESTE-01", "cod_turma": COD_TURMA},
    {"nome": "Aluno Teste 2", "turma": "TESTE-01", "cod_turma": COD_TURMA},
]


@pytest.fixture(scope="module")
def services():
    # A 1ª execução abre o device flow — as seguintes reutilizam o token em cache
    return AlunoService(), ChamadaService()


@pytest.fixture(scope="module")
def alunos_criados(services):
    aluno_svc, _ = services
    criados = []

    for dados in ALUNOS_PARA_CRIAR:
        aluno = aluno_svc.criar(dados)
        criados.append(aluno)
        print(f"  [+] Aluno criado: {aluno['nome']} (id={aluno['id']})")

    yield criados

    # Limpeza: remove os alunos criados pelo teste
    for aluno in criados:
        aluno_svc.deletar(aluno["id"])
        print(f"  [-] Aluno removido: {aluno['nome']} (id={aluno['id']})")


@pytest.fixture(scope="module")
def chamadas_registradas(services, alunos_criados):
    _, chamada_svc = services
    registradas = []

    for aluno in alunos_criados:
        chamada = chamada_svc.registrar(ChamadaCreate(
            nome_aluno=aluno["nome"],
            cod_turma=aluno["cod_turma"],
            data_aula=DATA_AULA,
            disciplina=DISCIPLINA,
            presente=False,  # começa como ausente
        ))
        registradas.append(chamada)
        print(f"  [+] Chamada registrada: {aluno['nome']} → ausente (id={chamada['ID']})")

    yield registradas

    # Limpeza: remove as chamadas criadas pelo teste
    for chamada in registradas:
        chamada_svc.sp.deletar(settings.CHAMADAS_LIST_NAME, chamada["ID"])
        print(f"  [-] Chamada removida: id={chamada['ID']}")


# ─────────────────────────────────────────────────────────────────────────────

def test_criar_dois_alunos(alunos_criados):
    assert len(alunos_criados) == 2
    for i, aluno in enumerate(alunos_criados, 1):
        assert aluno["id"] is not None
        assert aluno["nome"] == f"Aluno Teste {i}"
        assert aluno["cod_turma"] == COD_TURMA
    print("\n  OK: 2 alunos criados no SharePoint")


def test_registrar_chamada_para_os_dois(chamadas_registradas):
    assert len(chamadas_registradas) == 2
    for chamada in chamadas_registradas:
        assert chamada["ID"] is not None
        assert chamada["Presente"] is False
    print("\n  OK: chamadas registradas como ausente")


def test_atualizar_presenca_para_presente(services, chamadas_registradas):
    _, chamada_svc = services

    for chamada in chamadas_registradas:
        chamada_svc.atualizar_presenca(chamada["ID"], presente=True)
        print(f"  [~] Chamada {chamada['ID']} atualizada → presente")

    # Confirma no SharePoint que foi salvo
    todas = chamada_svc.sp.listar(settings.CHAMADAS_LIST_NAME)
    ids_atualizados = {c["ID"] for c in chamadas_registradas}

    for item in todas:
        if item.get("ID") in ids_atualizados:
            assert item["Presente"] is True, f"Chamada {item['ID']} não foi atualizada"

    print("\n  OK: todos os alunos marcados como presentes")

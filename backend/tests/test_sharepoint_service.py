import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def sp_service():
    with patch("app.services.sharepoint_service.get_sharepoint_context"), \
         patch("app.services.sharepoint_service.com_retry", side_effect=lambda fn: fn()):
        from app.services.sharepoint_service import SharePointService
        return SharePointService()


def test_listar_retorna_lista_de_propriedades(sp_service):
    item1 = MagicMock()
    item1.properties = {"ID": 1, "Nome_Aluno": "Ana"}
    item2 = MagicMock()
    item2.properties = {"ID": 2, "Nome_Aluno": "Bruno"}

    (sp_service.ctx.web.lists
        .get_by_title.return_value
        .items.get.return_value
        .execute_query.return_value) = [item1, item2]

    resultado = sp_service.listar("lst_alunos")

    assert len(resultado) == 2
    assert resultado[0]["Nome_Aluno"] == "Ana"
    assert resultado[1]["ID"] == 2


def test_criar_retorna_propriedades_do_item(sp_service):
    novo_item = MagicMock()
    novo_item.properties = {"ID": 99, "Nome_Aluno": "Carlos"}

    (sp_service.ctx.web.lists
        .get_by_title.return_value
        .add_item.return_value) = novo_item

    resultado = sp_service.criar("lst_alunos", {"Nome_Aluno": "Carlos"})

    assert resultado["ID"] == 99
    assert resultado["Nome_Aluno"] == "Carlos"


def test_atualizar_chama_set_property_e_update(sp_service):
    item_mock = MagicMock()
    (sp_service.ctx.web.lists
        .get_by_title.return_value
        .get_item_by_id.return_value) = item_mock

    sp_service.atualizar("lst_alunos", 1, {"Presente": True, "Disciplina": "Python"})

    item_mock.set_property.assert_any_call("Presente", True)
    item_mock.set_property.assert_any_call("Disciplina", "Python")
    item_mock.update.assert_called_once()


def test_deletar_chama_delete_object(sp_service):
    item_mock = MagicMock()
    (sp_service.ctx.web.lists
        .get_by_title.return_value
        .get_item_by_id.return_value) = item_mock

    sp_service.deletar("lst_alunos", 42)

    item_mock.delete_object.assert_called_once()
    sp_service.ctx.execute_query.assert_called()

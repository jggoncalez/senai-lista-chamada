from office365.sharepoint.client_context import ClientContext
from app.auth.microsoft_context import get_sharepoint_context
from app.utils.retry import com_retry

class SharePointService:
    def __init__(self):
        self.ctx: ClientContext = get_sharepoint_context()

    def listar(self, nome_lista: str) -> list[dict]:
        def _exec():
            items = (
                self.ctx.web
                .lists.get_by_title(nome_lista)
                .items.get()
                .execute_query()
            )
            return [item.properties for item in items]
        return com_retry(_exec)

    def criar(self, nome_lista: str, dados: dict) -> dict:
        def _exec():
            item = (
                self.ctx.web
                .lists.get_by_title(nome_lista)
                .add_item(dados)
            )
            self.ctx.execute_query()
            return item.properties
        return com_retry(_exec)

    def buscar_por_id(self, nome_lista: str, item_id: int) -> dict:
        def _exec():
            item = (
                self.ctx.web
                .lists.get_by_title(nome_lista)
                .get_item_by_id(item_id)
            )
            self.ctx.load(item)
            self.ctx.execute_query()
            return item.properties
        return com_retry(_exec)

    def atualizar(self, nome_lista: str, item_id: int, dados: dict) -> None:
        def _exec():
            item = (
                self.ctx.web
                .lists.get_by_title(nome_lista)
                .get_item_by_id(item_id)
            )
            for chave, valor in dados.items():
                item.set_property(chave, valor)
            item.update()
            self.ctx.execute_query()
        com_retry(_exec)

    def deletar(self, nome_lista: str, item_id: int) -> None:
        def _exec():
            (
                self.ctx.web
                .lists.get_by_title(nome_lista)
                .get_item_by_id(item_id)
                .delete_object()
            )
            self.ctx.execute_query()
        com_retry(_exec)
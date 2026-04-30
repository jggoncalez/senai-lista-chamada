from app.services.sharepoint_service import SharePointService
from app.config import settings

class AlunoService:
    def __init__(self):
        self.sp = SharePointService()

    def criar(self, dados: dict) -> dict:
        campos = {
            "Nome_Aluno": dados["nome"],
            "Turma": dados["turma"],
            "Cod_x002e_Turma": dados["cod_turma"],
        }
        # Campos opcionais — só envia se fornecidos para não conflitar com o tipo do SharePoint
        if "chamada" in dados:
            campos["Chamada"] = dados["chamada"]
        if "termo" in dados:
            campos["Termo"] = dados["termo"]

        raw = self.sp.criar(settings.ALUNOS_LIST_NAME, campos)
        return self._formatar([raw])[0]

    def listar_todos(self) -> list[dict]:
        items = self.sp.listar(settings.ALUNOS_LIST_NAME)
        return self._formatar(items)

    def listar_por_turma(self, turma: str) -> list[dict]:
        todos = self.sp.listar(settings.ALUNOS_LIST_NAME)
        filtrados = [a for a in todos if a.get("Cod_x002e_Turma") == turma]
        return self._formatar(filtrados)

    def buscar_por_id(self, item_id: int) -> dict:
        item = self.sp.buscar_por_id(settings.ALUNOS_LIST_NAME, item_id)
        return self._formatar([item])[0]

    def atualizar(self, item_id: int, dados: dict) -> None:
        campos = {}
        if "nome" in dados:
            campos["Nome_Aluno"] = dados["nome"]
        if "turma" in dados:
            campos["Turma"] = dados["turma"]
        if "cod_turma" in dados:
            campos["Cod_x002e_Turma"] = dados["cod_turma"]
        if "chamada" in dados:
            campos["Chamada"] = dados["chamada"]
        if "termo" in dados:
            campos["Termo"] = dados["termo"]

        if not campos:
            raise ValueError("Nenhum campo válido para atualizar.")

        self.sp.atualizar(settings.ALUNOS_LIST_NAME, item_id, campos)

    def deletar(self, item_id: int) -> None:
        self.buscar_por_id(item_id)
        self.sp.deletar(settings.ALUNOS_LIST_NAME, item_id)

    def _formatar(self, items: list[dict]) -> list[dict]:
        return [
            {
                "id":        item.get("ID"),
                "nome":      item.get("Nome_Aluno"),
                "turma":     item.get("Turma"),
                "cod_turma": item.get("Cod_x002e_Turma"),
                "chamada":   item.get("Chamada"),
                "termo":     item.get("Termo"),
            }
            for item in items
        ]
from app.services.sharepoint_service import SharePointService
from app.models.schemas import ChamadaCreate
from app.config import settings

class ChamadaService:
    def __init__(self):
        self.sp = SharePointService()

    def registrar(self, chamada: ChamadaCreate) -> dict:
        existentes = self.sp.listar(settings.CHAMADAS_LIST_NAME)
        ja_existe = any(
            c.get("Nome_Aluno")      == chamada.nome_aluno
            and c.get("Data_Aula")   == chamada.data_aula
            and c.get("Disciplina")  == chamada.disciplina
            for c in existentes
        )
        if ja_existe:
            raise ValueError("Chamada já registrada para este aluno nesta aula.")

        return self.sp.criar(settings.CHAMADAS_LIST_NAME, {
            "Nome_Aluno":      chamada.nome_aluno,
            "Cod_x002e_Turma": chamada.cod_turma,
            "Data_Aula":       chamada.data_aula,
            "Disciplina":      chamada.disciplina,
            "Presente":        chamada.presente,
        })

    def atualizar_presenca(self, item_id: int, presente: bool) -> None:
        self.sp.atualizar(settings.CHAMADAS_LIST_NAME, item_id, {"Presente": presente})

    def relatorio(self, cod_turma: str, data: str) -> list[dict]:
        todos = self.sp.listar(settings.CHAMADAS_LIST_NAME)
        return [
            c for c in todos
            if c.get("Cod_x002e_Turma") == cod_turma
            and c.get("Data_Aula", "").startswith(data)
        ]
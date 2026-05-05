from app.services.sharepoint_service import SharePointService
from app.utils.caml import caml_eq, caml_view
from app.config import settings

_F_NOME    = "Nome_Aluno"
_F_TURMA   = "Turma"
_F_COD     = "Cod_x002e_Turma"
_F_CHAMADA = "Chamada"

_CAMPO_MAP = {"nome": _F_NOME, "turma": _F_TURMA, "cod_turma": _F_COD}


class AlunoService:
    def __init__(self):
        self.sp = SharePointService()

    def criar(self, dados: dict) -> dict:
        campos = {
            _F_NOME:  dados["nome"],
            _F_TURMA: dados["turma"],
            _F_COD:   dados["cod_turma"],
        }
        if dados.get("chamada") is not None:
            campos[_F_CHAMADA] = str(dados["chamada"])

        raw = self.sp.criar(settings.ALUNOS_LIST_NAME, campos)
        return self._formatar([raw])[0]

    def listar_todos(self) -> list[dict]:
        items = self.sp.listar(settings.ALUNOS_LIST_NAME)
        return self._formatar(items)

    def listar_por_turma(self, turma: str) -> list[dict]:
        filtro = caml_view(caml_eq(_F_COD, "Text", turma))
        items = self.sp.listar(settings.ALUNOS_LIST_NAME, filtro_caml=filtro)
        return self._formatar(items)

    def buscar_por_id(self, item_id: int) -> dict:
        item = self.sp.buscar_por_id(settings.ALUNOS_LIST_NAME, item_id)
        return self._formatar([item])[0]

    def atualizar(self, item_id: int, dados: dict) -> None:
        campos = {_CAMPO_MAP[k]: v for k, v in dados.items() if k in _CAMPO_MAP}
        if "chamada" in dados:
            campos[_F_CHAMADA] = str(dados["chamada"]) if dados["chamada"] is not None else None

        if not campos:
            raise ValueError("Nenhum campo válido para atualizar.")

        self.sp.atualizar(settings.ALUNOS_LIST_NAME, item_id, campos)

    def deletar(self, item_id: int) -> None:
        # SharePointService.deletar lança exceção se o item não existe;
        # o router captura e mapeia para 404.
        self.sp.deletar(settings.ALUNOS_LIST_NAME, item_id)

    def _formatar(self, items: list[dict]) -> list[dict]:
        def para_int(valor):
            try:
                return int(valor)
            except (TypeError, ValueError):
                return None

        def para_str(valor):
            return str(valor) if valor is not None else None

        return [
            {
                "id":        para_int(item.get("ID")),
                "nome":      para_str(item.get(_F_NOME)),
                "turma":     para_str(item.get(_F_TURMA)),
                "cod_turma": para_str(item.get(_F_COD)),
                "chamada":   para_int(item.get(_F_CHAMADA)),
            }
            for item in items
        ]

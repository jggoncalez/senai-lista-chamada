from app.services.sharepoint_service import SharePointService
from app.models.schemas import ChamadaCreate
from app.utils.caml import caml_eq, caml_eq_date, caml_and, caml_view
from app.config import settings

_F_NOME       = "Nome_Aluno"
_F_COD        = "Cod_x002e_Turma"
_F_DATA       = "Data_Aula"
_F_DISCIPLINA = "Disciplina"
_F_PRESENTE   = "Presente"


class ChamadaService:
    def __init__(self):
        self.sp = SharePointService()

    def registrar(self, chamada: ChamadaCreate) -> dict:
        filtro = caml_view(
            caml_and(
                caml_eq(_F_NOME, "Text", chamada.nome_aluno),
                caml_eq_date(_F_DATA, chamada.data_aula.isoformat()),
                caml_eq(_F_DISCIPLINA, "Text", chamada.disciplina),
            )
        )
        if self.sp.listar(settings.CHAMADAS_LIST_NAME, filtro_caml=filtro):
            raise ValueError("Chamada já registrada para este aluno nesta aula.")

        return self.sp.criar(settings.CHAMADAS_LIST_NAME, {
            _F_NOME:       chamada.nome_aluno,
            _F_COD:        chamada.cod_turma,
            _F_DATA:       chamada.data_aula.isoformat(),
            _F_DISCIPLINA: chamada.disciplina,
            _F_PRESENTE:   chamada.presente,
        })

    def atualizar_presenca(self, item_id: int, presente: bool) -> None:
        self.sp.atualizar(settings.CHAMADAS_LIST_NAME, item_id, {_F_PRESENTE: presente})

    def relatorio(self, cod_turma: str, data: str) -> list[dict]:
        filtro = caml_view(caml_eq(_F_COD, "Text", cod_turma))
        registros = self.sp.listar(settings.CHAMADAS_LIST_NAME, filtro_caml=filtro)
        # Filtragem por data feita em Python para evitar ambiguidades de timezone
        # que o CAML DateTime introduziria ao comparar datas ISO 8601 com offset.
        return [c for c in registros if c.get(_F_DATA, "").startswith(data)]

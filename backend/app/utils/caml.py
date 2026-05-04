"""Filtragem pelo Sharepoint
Sharepoint usa CAML (Collaborative Application Markup Language) para consultas. Esta função ajuda a construir expressões CAML para filtrar itens com base em campos de texto, número ou data."""
import html as _html

def caml_eq(field: str, tipo: str, valor: str) -> str:
    """Condição de igualdade para campos de texto ou número."""
    return f"<Eq><FieldRef Name='{field}'/><Value Type='{tipo}'>{_html.escape(valor)}</Value></Eq>"


def caml_eq_date(field: str, data_iso: str) -> str:
    """Condição de igualdade para campos DateTime, ignorando o horário."""
    return (
        f"<Eq><FieldRef Name='{field}'/>"
        f"<Value Type='DateTime' IncludeTimeValue='FALSE'>{_html.escape(data_iso)}</Value></Eq>"
    )


def caml_and(*conds: str) -> str:
    """Combina condições com AND. CAML And é binário — aninha recursivamente."""
    if len(conds) == 1:
        return conds[0]
    return f"<And>{conds[0]}{caml_and(*conds[1:])}</And>"


def caml_view(*conds: str) -> str:
    """Envolve condições em um bloco CAML View/Query/Where completo."""
    if not conds:
        return "<View/>"
    where = caml_and(*conds) if len(conds) > 1 else conds[0]
    return f"<View><Query><Where>{where}</Where></Query></View>"

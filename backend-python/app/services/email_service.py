import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.sessao_aula import SessaoAula
from app.models.presenca import PresencaAluno
from app.models.turma_disciplina import TurmaDisciplina
from app.models.turma import Turma
from app.models.curso import Curso
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.services.teams_service import _gerar_resumo_ia

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def _calcular_frequencia_semana(
    db: Session, turma_id: int, inicio: date, fim: date
) -> dict:
    sessoes = (
        db.query(SessaoAula)
        .join(TurmaDisciplina, TurmaDisciplina.id == SessaoAula.turma_disciplina_id)
        .filter(
            TurmaDisciplina.turma_id == turma_id,
            SessaoAula.data_aula >= inicio,
            SessaoAula.data_aula <= fim,
        )
        .all()
    )

    if not sessoes:
        return {}

    sessao_ids = [s.id for s in sessoes]

    presencas = (
        db.query(PresencaAluno)
        .filter(PresencaAluno.sessao_id.in_(sessao_ids))
        .all()
    )

    alunos_map: dict[int, dict] = {}
    for p in presencas:
        if p.aluno_id not in alunos_map:
            aluno = db.query(Aluno).filter(Aluno.id == p.aluno_id).first()
            alunos_map[p.aluno_id] = {
                "nome": aluno.nome if aluno else "?",
                "total": 0,
                "presentes": 0
            }
        alunos_map[p.aluno_id]["total"] += 1
        if p.presente:
            alunos_map[p.aluno_id]["presentes"] += 1

    return alunos_map


def _gerar_html_relatorio(
    turma: str,
    disciplina: str,
    inicio: str,
    fim: str,
    alunos_map: dict,
    resumo_ia: str
) -> str:
    total_geral = sum(a["total"] for a in alunos_map.values())
    presentes_geral = sum(a["presentes"] for a in alunos_map.values())
    pct_geral = (presentes_geral / total_geral * 100) if total_geral > 0 else 0

    alunos_risco = [
        {"nome": a["nome"], "pct": (a["presentes"] / a["total"] * 100)}
        for a in alunos_map.values()
        if a["total"] > 0 and (a["presentes"] / a["total"] * 100) < 75
    ]

    linhas_alunos = ""
    for a in alunos_map.values():
        pct = (a["presentes"] / a["total"] * 100) if a["total"] > 0 else 0
        cor = "#dc2626" if pct < 75 else "#16a34a"
        linhas_alunos += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #e5e7eb">{a['nome']}</td>
            <td style="padding:8px;border-bottom:1px solid #e5e7eb;text-align:center">{a['presentes']}/{a['total']}</td>
            <td style="padding:8px;border-bottom:1px solid #e5e7eb;text-align:center;color:{cor};font-weight:bold">{pct:.1f}%</td>
        </tr>
        """

    linhas_risco = "".join(
        f"<li style='color:#dc2626'>{a['nome']} — {a['pct']:.1f}%</li>"
        for a in alunos_risco
    ) or "<li style='color:#16a34a'>Nenhum aluno em risco esta semana ✅</li>"

    return f"""
    <html>
    <body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#1f2937">

        <div style="background:#dc2626;padding:24px;border-radius:8px 8px 0 0">
            <h1 style="color:white;margin:0;font-size:20px">📋 Relatório Semanal de Frequência</h1>
            <p style="color:#fecaca;margin:4px 0 0">SENAI — Sistema de Chamada</p>
        </div>

        <div style="background:#f9fafb;padding:20px;border:1px solid #e5e7eb">
            <table style="width:100%">
                <tr>
                    <td><strong>Turma:</strong> {turma}</td>
                    <td><strong>Disciplina:</strong> {disciplina}</td>
                </tr>
                <tr>
                    <td><strong>Período:</strong> {inicio} até {fim}</td>
                    <td><strong>Frequência geral:</strong>
                        <span style="color:{'#16a34a' if pct_geral >= 75 else '#dc2626'};font-weight:bold">
                            {pct_geral:.1f}%
                        </span>
                    </td>
                </tr>
            </table>
        </div>

        <div style="padding:20px;border:1px solid #e5e7eb;border-top:none">
            <h2 style="font-size:16px;color:#374151">👥 Frequência por Aluno</h2>
            <table style="width:100%;border-collapse:collapse">
                <thead>
                    <tr style="background:#f3f4f6">
                        <th style="padding:8px;text-align:left;font-size:12px;color:#6b7280;text-transform:uppercase">Aluno</th>
                        <th style="padding:8px;text-align:center;font-size:12px;color:#6b7280;text-transform:uppercase">Presenças</th>
                        <th style="padding:8px;text-align:center;font-size:12px;color:#6b7280;text-transform:uppercase">%</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_alunos}
                </tbody>
            </table>
        </div>

        <div style="padding:20px;border:1px solid #e5e7eb;border-top:none;background:#fff7ed">
            <h2 style="font-size:16px;color:#dc2626">⚠️ Alunos abaixo de 75%</h2>
            <ul style="margin:0;padding-left:20px">
                {linhas_risco}
            </ul>
        </div>

        <div style="padding:20px;border:1px solid #e5e7eb;border-top:none;background:#eff6ff">
            <h2 style="font-size:16px;color:#1d4ed8">🤖 Análise IA</h2>
            <p style="color:#374151;line-height:1.6">{resumo_ia}</p>
        </div>

        <div style="padding:16px;text-align:center;color:#9ca3af;font-size:12px">
            Gerado automaticamente pelo Sistema de Chamada SENAI Limeira
        </div>

    </body>
    </html>
    """


def enviar_relatorio_semanal(db: Session):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("⚠️ EMAIL_USER ou EMAIL_PASSWORD não configurados.")
        return

    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=4)

    turma_disciplinas = (
        db.query(TurmaDisciplina)
        .filter(TurmaDisciplina.ativo == True)
        .all()
    )

    for td in turma_disciplinas:
        professor = db.query(Usuario).filter(
            Usuario.id == td.professor_id
        ).first()

        if not professor or not str(professor.email):
            continue

        turma = db.query(Turma).filter(Turma.id == td.turma_id).first()
        curso = db.query(Curso).filter(Curso.id == td.curso_id).first()

        if not turma or not curso:
            continue

        turma_id_val: int = td.turma_id  # type: ignore
        alunos_map = _calcular_frequencia_semana(
            db, turma_id_val, inicio_semana, fim_semana
        )

        if not alunos_map:
            continue

        total = sum(a["total"] for a in alunos_map.values())
        presentes = sum(a["presentes"] for a in alunos_map.values())

        alunos_risco = [
            {"nome": a["nome"], "pct": (a["presentes"] / a["total"] * 100)}
            for a in alunos_map.values()
            if a["total"] > 0 and (a["presentes"] / a["total"] * 100) < 75
        ]

        resumo_ia = _gerar_resumo_ia(
            turma=str(turma.cod_turma),
            disciplina=str(curso.nome),
            data=f"{inicio_semana} a {fim_semana}",
            total=len(alunos_map),
            presentes=presentes,
            alunos_risco=alunos_risco
        )

        html = _gerar_html_relatorio(
            turma=str(turma.cod_turma),
            disciplina=str(curso.nome),
            inicio=str(inicio_semana),
            fim=str(fim_semana),
            alunos_map=alunos_map,
            resumo_ia=resumo_ia
        )

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"📋 Relatório Semanal — {turma.cod_turma} | {curso.nome}"
            msg["From"] = EMAIL_USER
            msg["To"] = str(professor.email)
            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.sendmail(
                    EMAIL_USER,
                    str(professor.email),
                    msg.as_string()
                )

            print(f"✅ Email enviado para {professor.email} — {turma.cod_turma}")

        except Exception as e:
            print(f"❌ Erro ao enviar email para {professor.email}: {e}")
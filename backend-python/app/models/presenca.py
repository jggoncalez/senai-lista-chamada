from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class PresencaAluno(Base):
    __tablename__ = "presenca_alunos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sessao_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessao_aula.id"), nullable=False)
    aluno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alunos.id"), nullable=False)
    faltas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    observacao: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("sessao_id", "aluno_id", name="uq_presenca"),
    )

    sessao = relationship("SessaoAula", back_populates="presencas")
    aluno = relationship("Aluno", back_populates="presencas")
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class PresencaAluno(Base):
    __tablename__ = "presenca_alunos"

    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(Integer, ForeignKey("sessao_aula.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    presente = Column(Boolean, nullable=False)
    observacao = Column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("sessao_id", "aluno_id", name="uq_presenca"),
    )

    sessao = relationship("SessaoAula", back_populates="presencas")
    aluno = relationship("Aluno", back_populates="presencas")

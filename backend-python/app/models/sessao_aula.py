from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SessaoAula(Base):
    __tablename__ = "sessao_aula"

    id = Column(Integer, primary_key=True, index=True)
    turma_disciplina_id = Column(Integer, ForeignKey("turma_disciplina.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_aula = Column(Date, nullable=False)
    observacao = Column(String(500), nullable=True)
    registrado_em = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("turma_disciplina_id", "data_aula", name="uq_sessao"),
    )

    turma_disciplina = relationship("TurmaDisciplina", back_populates="sessoes")
    professor = relationship("Usuario", back_populates="sessoes_registradas")
    presencas = relationship("PresencaAluno", back_populates="sessao")

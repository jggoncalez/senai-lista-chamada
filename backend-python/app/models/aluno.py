from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    turma_id = Column(Integer, ForeignKey("turma.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    empresa = Column(String(100), nullable=True)
    ra = Column(String(50), unique=True, nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now())

    turma = relationship("Turma", back_populates="alunos")
    presencas = relationship("PresencaAluno", back_populates="aluno")
    disciplinas_extra = relationship("AlunoDisciplinaExtra", back_populates="aluno")

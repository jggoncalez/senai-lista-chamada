from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Turma(Base):
    __tablename__ = "turma"

    id = Column(Integer, primary_key=True, index=True)
    cod_turma = Column(String(50), unique=True, nullable=True)
    nome_turma = Column(String(200), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=True)
    termo = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now())

    curso = relationship("Curso", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma")
    disciplinas = relationship("TurmaDisciplina", back_populates="turma")
    alunos_extra_disciplina = relationship("AlunoDisciplinaExtra", back_populates="turma")

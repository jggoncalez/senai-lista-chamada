from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    eixo_tecnologico = Column(String(200), nullable=True)
    duracao_termos = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())

    turmas = relationship("Turma", back_populates="curso")
    turma_disciplinas = relationship("TurmaDisciplina", back_populates="curso")
    alunos_extra = relationship("AlunoDisciplinaExtra", back_populates="curso")

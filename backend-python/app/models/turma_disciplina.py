from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class TurmaDisciplina(Base):
    __tablename__ = "turma_disciplina"

    id = Column(Integer, primary_key=True, index=True)
    turma_id = Column(Integer, ForeignKey("turma.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    dia_semana = Column(Integer, nullable=True)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("turma_id", "curso_id", "dia_semana", name="uq_turma_disciplina"),
    )

    turma = relationship("Turma", back_populates="disciplinas")
    curso = relationship("Curso", back_populates="turma_disciplinas")
    professor = relationship("Usuario", back_populates="turma_disciplinas")
    sessoes = relationship("SessaoAula", back_populates="turma_disciplina")

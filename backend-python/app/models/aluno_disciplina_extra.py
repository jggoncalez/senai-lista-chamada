from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class AlunoDisciplinaExtra(Base):
    __tablename__ = "aluno_disciplina_extra"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turma.id"), nullable=True)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("aluno_id", "curso_id", name="uq_aluno_extra"),
    )

    aluno = relationship("Aluno", back_populates="disciplinas_extra")
    curso = relationship("Curso", back_populates="alunos_extra")
    turma = relationship("Turma", back_populates="alunos_extra_disciplina")

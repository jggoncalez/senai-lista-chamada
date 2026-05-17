from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    azure_object_id = Column(String(100), unique=True, nullable=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())

    role = relationship("Role", back_populates="usuarios")
    turma_disciplinas = relationship("TurmaDisciplina", back_populates="professor")
    sessoes_registradas = relationship("SessaoAula", back_populates="professor")

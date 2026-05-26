from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def listar(db: Session, apenas_ativos: bool = True) -> list[Usuario]:
    q = db.query(Usuario)
    if apenas_ativos:
        q = q.filter(Usuario.ativo == True)
    return q.all()


def buscar(db: Session, usuario_id: int) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


def buscar_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def criar(db: Session, dados: UsuarioCreate) -> Usuario:
    existente = buscar_por_email(db, dados.email)
    if existente:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    usuario = Usuario(**dados.model_dump())
    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, usuario_id: int, dados: UsuarioUpdate) -> Usuario:
    usuario = buscar(db, usuario_id)
    campos = dados.model_dump(exclude_unset=True)
    if not campos:
        return usuario
    if "email" in campos and campos["email"] != usuario.email:
        existente = buscar_por_email(db, campos["email"])
        if existente:
            raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    for campo, valor in campos.items():
        setattr(usuario, campo, valor)
    try:
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, usuario_id: int) -> None:
    usuario = buscar(db, usuario_id)
    usuario.ativo = False
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

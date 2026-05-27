from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.role import Role

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
def get_me(db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == "sistema@senai.br").first()
    if not user:
        role = db.query(Role).filter(Role.nome == "professor").first()
        if not role:
            role = db.query(Role).first()
        user = Usuario(
            nome="Professor Sistema",
            email="sistema@senai.br",
            role_id=role.id,
            ativo=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "roles": [user.role.nome] if user.role else ["professor"]
    }
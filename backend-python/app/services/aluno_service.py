from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.aluno import Aluno
from app.models.turma import Turma
from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoImport


def listar(db: Session, turma_cod: str | None = None, apenas_ativos: bool = True) -> list[dict]:
    q = db.query(Aluno).options(joinedload(Aluno.turma))
    if apenas_ativos:
        q = q.filter(Aluno.ativo == True)
    if turma_cod is not None:
        q = q.join(Turma).filter(Turma.cod_turma == turma_cod)
    
    alunos = q.all()
    
    # Mapear para o formato que o schema AlunoResponse espera (com turma e cod_turma)
    resultado = []
    for a in alunos:
        aluno_dict = {
            "id": a.id,
            "turma_id": a.turma_id,
            "nome": a.nome,
            "empresa": a.empresa,
            "ra": a.ra,
            "chamada": None,
            "ativo": a.ativo,
            "criado_em": a.criado_em,
            "atualizado_em": a.atualizado_em,
            "turma": a.turma.nome_turma if a.turma else None,
            "cod_turma": a.turma.cod_turma if a.turma else None
        }
        resultado.append(aluno_dict)
    
    return resultado


def buscar(db: Session, aluno_id: int) -> Aluno:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def criar(db: Session, dados: AlunoCreate) -> Aluno:
    if dados.ra:
        existente = db.query(Aluno).filter(Aluno.ra == dados.ra).first()
        if existente:
            raise HTTPException(status_code=409, detail="RA já cadastrado")
    aluno = Aluno(**dados.model_dump(exclude={"chamada"}))  # ← exclui chamada
    try:
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        return aluno
    except Exception:
        db.rollback()
        raise


def atualizar(db: Session, aluno_id: int, dados: AlunoUpdate) -> Aluno:
    aluno = buscar(db, aluno_id)
    campos = dados.model_dump(exclude_unset=True, exclude={"chamada"})  # ← exclui chamada
    ...
    if not campos:
        return aluno
    if "ra" in campos and campos["ra"] != aluno.ra and campos["ra"] is not None:
        existente = db.query(Aluno).filter(Aluno.ra == campos["ra"]).first()
        if existente:
            raise HTTPException(status_code=409, detail="RA já cadastrado")
    campos["atualizado_em"] = datetime.utcnow()
    for campo, valor in campos.items():
        setattr(aluno, campo, valor)
    try:
        db.commit()
        db.refresh(aluno)
        return aluno
    except Exception:
        db.rollback()
        raise


def desativar(db: Session, aluno_id: int) -> None:
    aluno = buscar(db, aluno_id)
    aluno.ativo = False
    aluno.atualizado_em = datetime.utcnow()
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

def importar_lote(db: Session, dados: list[AlunoImport]):
    total = len(dados)
    sucesso = 0
    erro = 0
    detalhes = []

    for item in dados:
        try:
            # 1. Buscar ou criar turma
            turma = db.query(Turma).filter(Turma.cod_turma == item.cod_turma).first()
            if not turma:
                turma = Turma(
                    cod_turma=item.cod_turma,
                    nome_turma=item.turma,
                    termo=item.termo or 1
                )
                db.add(turma)
                db.flush()
            
            # 2. Verificar se aluno já existe na turma (por nome)
            aluno = db.query(Aluno).filter(
                Aluno.nome == item.nome,
                Aluno.turma_id == turma.id
            ).first()

            if not aluno:
                aluno = Aluno(
                    nome=item.nome,
                    turma_id=turma.id,
                    ra=item.ra or None,
                    ativo=True
                )
                db.add(aluno)
                sucesso += 1
                detalhes.append({"nome": item.nome, "status": "sucesso", "mensagem": "Criado"})
            else:
                aluno.ativo = True
                sucesso += 1
                detalhes.append({"nome": item.nome, "status": "sucesso", "mensagem": "Atualizado"})
            
        except Exception as e:
            erro += 1
            detalhes.append({"nome": item.nome, "status": "erro", "mensagem": str(e)})
            db.rollback()
            continue

    db.commit()
    return {
        "total": total,
        "sucesso": sucesso,
        "erro": erro,
        "detalhes": detalhes
    }

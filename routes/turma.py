from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models.turma import Turma
from models.tutor import Tutor
from database import get_session
from datetime import datetime

router = APIRouter(
    prefix="/turmas",  # Prefixo para todas as rotas
    tags=["Turmas"],   # Tag para documentação automática
)

# Criar turma
@router.post("/", response_model=Turma)
def create_turma(turma: Turma, session: Session = Depends(get_session)):
    session.add(turma)
    session.commit()
    session.refresh(turma)
    return turma
# Listar turmas
@router.get("/", response_model=list[Turma])
def read_turmas(offset: int = 0, limit: int = Query(default=10, le=100), 
               session: Session = Depends(get_session)):
    statement = (select(Turma).offset(offset).limit(limit)
                 .options(joinedload(Turma.alunos), joinedload(Turma.tutor)))
    return session.exec(statement).unique().all()
# Ler turma por id
@router.get("/{turma_id}", response_model=Turma)
def read_turma(turma_id: int, session: Session = Depends(get_session)):
    statement = (select(Turma).where(Turma.id == turma_id)
                 .options(joinedload(Turma.alunos), joinedload(Turma.tutor)))
    turma = session.exec(statement).first()
    if not turma:
        raise HTTPException(status_code=404, detail="turma not found")
    return turma
# Atualizar turma
@router.put("/{turma_id}", response_model=Turma)
def update_turma(turma_id: int, turma: Turma, session: Session = Depends(get_session)):
    db_turma = session.get(Turma, turma_id)
    if not db_turma:
        raise HTTPException(status_code=404, detail="turma not found")
    for key, value in turma.dict(exclude_unset=True).items():
        setattr(db_turma, key, value)
    db_turma.updated_at = datetime.utcnow()
    session.add(db_turma)
    session.commit()
    session.refresh(db_turma)
    return db_turma
# Deletar turma
@router.delete("/{turma_id}")
def delete_turma(turma_id: int, session: Session = Depends(get_session)):
    turma = session.get(Turma, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="turma not found")
    session.delete(turma)
    session.commit()
    return {"ok": True}

# Adicionar tutor a turma
@router.put("/{turma_id}/tutor/{tutor_id}", response_model=Turma)
def add_tutor(turma_id: int, tutor_id: int, session: Session = Depends(get_session)):
    turma = session.get(Turma, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="turma not found")
    tutor = session.get(Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="tutor not found")
    turma.tutor = tutor
    session.add(turma)
    session.commit()
    session.refresh(turma)
    return turma
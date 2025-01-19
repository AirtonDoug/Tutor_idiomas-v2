from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.tutor import Tutor
from models.turma import Turma
from models.aluno import Aluno
from database import get_session

router = APIRouter(
    prefix="/tutors",  # Prefixo para todas as rotas
    tags=["Tutors"],   # Tag para documentação automática
)

# Tutors
@router.post("/", response_model=Tutor)
def create_tutor(tutor: Tutor, session: Session = Depends(get_session)):
    session.add(tutor)
    session.commit()
    session.refresh(tutor)
    return tutor

@router.get("/", response_model=list[Tutor])
def read_tutors(offset: int = 0, limit: int = Query(default=10, le=100), 
                session: Session = Depends(get_session)):
    return session.exec(select(Tutor).offset(offset).limit(limit)).all()

@router.get("/{tutor_id}", response_model=Tutor)
def read_tutor(tutor_id: int, session: Session = Depends(get_session)):
    tutor = session.get(Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor

@router.put("/{tutor_id}", response_model=Tutor)
def update_tutor(tutor_id: int, tutor: Tutor, session: Session = Depends(get_session)):
    db_tutor = session.get(Tutor, tutor_id)
    if not db_tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    for key, value in tutor.dict(exclude_unset=True).items():
        setattr(db_tutor, key, value)
    session.add(db_tutor)
    session.commit()
    session.refresh(db_tutor)
    return db_tutor

@router.delete("/{tutor_id}")
def delete_tutor(tutor_id: int, session: Session = Depends(get_session)):
    tutor = session.get(Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    session.delete(tutor)
    session.commit()
    return {"ok": True}

# Obter todas as turmas de um tutor específico
@router.get("/{tutor_id}/turmas", response_model=list[Turma])
def get_turmas_por_tutor(tutor_id: int, session: Session = Depends(get_session)):
    statement = select(Turma).where(Turma.tutor_id == tutor_id)
    turmas = session.exec(statement).all()
    if not turmas:
        raise HTTPException(status_code=404, detail="No turmas found for this tutor")
    return turmas

# Obter todos os alunos de um tutor específico
@router.get("/{tutor_id}/alunos", response_model=list[Aluno])
def get_alunos_por_tutor(tutor_id: int, session: Session = Depends(get_session)):
    statement = select(Aluno).join(Turma).where(Turma.tutor_id == tutor_id)
    alunos = session.exec(statement).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="No alunos found for this tutor")
    return alunos
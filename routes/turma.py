from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models.turma import Turma, TurmaConversation, TurmaBaseWithTutorAlunosConversations
from models.aluno import Aluno
from models.conversation import Conversation
from database import get_session
from datetime import datetime

router = APIRouter(
    prefix="/turmas",  # Prefixo para todas as rotas
    tags=["Turmas"],   # Tag para documentação automática
)

# Turmas
@router.post("/", response_model=Turma)
def create_turma(turma: Turma, session: Session = Depends(get_session)):
    session.add(turma)
    session.commit()
    session.refresh(turma)
    return turma

@router.get("/", response_model=list[TurmaBaseWithTutorAlunosConversations])
def read_turmas(offset: int = 0, limit: int = Query(default=10, le=100), 
                session: Session = Depends(get_session)):
    return session.exec(select(Turma).offset(offset).limit(limit)).all()

@router.get("/{turma_id}", response_model=TurmaBaseWithTutorAlunosConversations)
def read_turma(turma_id: int, session: Session = Depends(get_session)):
    turma = session.get(Turma, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma not found")
    return turma

@router.put("/{turma_id}", response_model=Turma)
def update_turma(turma_id: int, turma: Turma, session: Session = Depends(get_session)):
    db_turma = session.get(Turma, turma_id)
    if not db_turma:
        raise HTTPException(status_code=404, detail="Turma not found")
    for key, value in turma.dict(exclude_unset=True).items():
        setattr(db_turma, key, value)
    db_turma.updated_at = datetime.utcnow()
    session.add(db_turma)
    session.commit()
    session.refresh(db_turma)
    return db_turma

# retornar tutor e nivel da turma pelo nome da turma
@router.get("/nome/{nome_turma}", response_model=dict)
def get_tutor_and_nivel_by_nome_turma(nome_turma: str, session: Session = Depends(get_session)):
    turma = session.exec(select(Turma).where(Turma.nome == nome_turma).options(joinedload(Turma.tutor))).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma not found")
    return {"tutor": turma.tutor.name, "lingua": turma.tutor.lingua, "nivel": turma.nivel}

# Quantidade total de alunos em uma turma
@router.get("/{turma_id}/alunos/quantidade", response_model=dict)
def get_total_alunos_for_turma(turma_id: int, session: Session = Depends(get_session)):
    total_alunos = len(session.exec(select(Aluno).where(Aluno.turma_id == turma_id)).all())
    return {"total_alunos": total_alunos}


@router.delete("/{turma_id}")
def delete_turma(turma_id: int, session: Session = Depends(get_session)):
    turma = session.get(Turma, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma not found")
    session.delete(turma)
    session.commit()
    return {"ok": True}

# Alunos
@router.post("/{turma_id}/alunos/", response_model=Aluno)
def create_aluno_for_turma(turma_id: int, aluno: Aluno, session: Session = Depends(get_session)):
    aluno.turma_id = turma_id
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    return aluno

@router.get("/{turma_id}/alunos/", response_model=list[Aluno])
def read_alunos_for_turma(turma_id: int, offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    return session.exec(select(Aluno).where(Aluno.turma_id == turma_id).offset(offset).limit(limit)).all()

@router.get("/aluno/{aluno_id}", response_model=Aluno)
def read_aluno_by_id(aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return aluno


# Buscar alunos por texto parcial
@router.get("/alunos/busca", response_model=list[Aluno])
def search_alunos(texto: str, session: Session = Depends(get_session)):
    statement = select(Aluno).where(Aluno.nome.contains(texto))
    alunos = session.exec(statement).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="No alunos found")
    return alunos

@router.put("/{turma_id}/alunos/{aluno_id}", response_model=Aluno)
def update_aluno_for_turma(turma_id: int, aluno_id: int, aluno: Aluno, session: Session = Depends(get_session)):
    db_aluno = session.get(Aluno, aluno_id)
    if not db_aluno or db_aluno.turma_id != turma_id:
        raise HTTPException(status_code=404, detail="Aluno not found")
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(db_aluno, key, value)
    db_aluno.updated_at = datetime.utcnow()
    session.add(db_aluno)
    session.commit()
    session.refresh(db_aluno)
    return db_aluno


@router.delete("/{turma_id}/alunos/{aluno_id}")
def delete_aluno_for_turma(turma_id: int, aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno or aluno.turma_id != turma_id:
        raise HTTPException(status_code=404, detail="Aluno not found")
    session.delete(aluno)
    session.commit()
    return {"ok": True}

@router.put("/{aluno_id}/trocar-turma", response_model=Aluno)
def trocar_turma_de_aluno(
    aluno_id: int,
    nova_turma_id: int,
    session: Session = Depends(get_session),
):
    db_aluno = session.get(Aluno, aluno_id)
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    nova_turma = session.get(Turma, nova_turma_id)
    if not nova_turma:
        raise HTTPException(status_code=404, detail="Nova turma não encontrada")


    db_aluno.turma_id = nova_turma_id

    session.add(db_aluno)
    session.commit()
    session.refresh(db_aluno)

    return db_aluno


# Conversations
@router.post("/{turma_id}/conversations/", response_model=Conversation)
def create_conversation_for_turma(turma_id: int, conversation: Conversation, session: Session = Depends(get_session)):
    conversation_db = session.exec(select(Conversation).where(Conversation.name == conversation.name)).first()
    if conversation_db:
        conversation = conversation_db
    else:
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    conversation_dump = conversation.model_dump()
    turma_conversation = TurmaConversation(turma_id=turma_id, conversation_id=conversation.id)
    session.add(turma_conversation)
    session.commit()
    return conversation_dump

@router.get("/{turma_id}/conversations/", response_model=list[Conversation])
def read_conversations_for_turma(turma_id: int, session: Session = Depends(get_session)):
    statement = select(Conversation).join(TurmaConversation).where(TurmaConversation.turma_id == turma_id)
    return session.exec(statement).all()


# Filtros por data/ano para Conversation
@router.get("/{turma_id}/conversations/data", response_model=list[Conversation])
def get_conversations_por_intervalo(
    turma_id: int,
    start_date: datetime, 
    end_date: datetime, 
    session: Session = Depends(get_session)
):
    statement = select(Conversation).join(TurmaConversation).where(
        TurmaConversation.turma_id == turma_id,
        Conversation.data_horario >= start_date.strftime("%Y-%m-%d %H:%M:%S"),
        Conversation.data_horario <= end_date.strftime("%Y-%m-%d %H:%M:%S")
    )
    conversations = session.exec(statement).all()
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found in this date range for the specified turma")
    return conversations

@router.put("/{turma_id}/conversations/{conversation_id}", response_model=Conversation)
def update_conversation_for_turma(turma_id: int, conversation_id: int, conversation: Conversation, session: Session = Depends(get_session)):
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    for key, value in conversation.model_dump(exclude_unset=True).items():
        setattr(db_conversation, key, value)
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation

@router.delete("/{turma_id}/conversations/{conversation_id}")
def delete_conversation_for_turma(turma_id: int, conversation_id: int, session: Session = Depends(get_session)):
    turma_conversation = session.exec(select(TurmaConversation).where(TurmaConversation.turma_id == turma_id, TurmaConversation.conversation_id == conversation_id)).first()
    if not turma_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found for this turma")
    session.delete(turma_conversation)
    session.commit()
    return {"ok": True}
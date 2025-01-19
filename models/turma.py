from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from .tutor import Tutor, TutorBase
from .aluno import Aluno, AlunoBaseWithTutor
from .conversation import Conversation

class TurmaConversation(SQLModel, table=True):
    turma_id: int = Field(default=None, foreign_key="turma.id", primary_key=True)
    conversation_id: int = Field(default=None, foreign_key="conversation.id", primary_key=True)

class TurmaBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Turma(TurmaBase, table=True):
    tutor_id: int = Field(foreign_key="tutor.id")
    tutor: 'Tutor' = Relationship(back_populates="turmas")
    alunos: list[Aluno] = Relationship(back_populates="turma")
    conversations: list[Conversation] = Relationship(link_model=TurmaConversation)

class TurmaBaseWithTutorAlunosConversations(TurmaBase):
    tutor: TutorBase | None
    alunos: list[AlunoBaseWithTutor] = None
    conversations: list[Conversation] = None
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from .tutor import Tutor, TutorBase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .turma import Turma

class AlunoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Aluno(AlunoBase, table=True):
    turma_id: int = Field(foreign_key="turma.id")
    tutor_id: int = Field(foreign_key="tutor.id")
    turma: 'Turma' = Relationship(back_populates="alunos")
    tutor: Tutor = Relationship(back_populates="alunos")

class AlunoBaseWithTutor(AlunoBase):
    tutor: TutorBase
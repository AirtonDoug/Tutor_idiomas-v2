
from sqlmodel import SQLModel, Field, Relationship
from .tutor import Tutor, TutorBase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .turma import Turma

class AlunoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    nickname: str
    


class Aluno(AlunoBase, table=True):
    turma_id: int = Field(foreign_key="turma.id")
    tutor_id: int = Field(foreign_key="tutor.id")
    turma: 'Turma' = Relationship(back_populates="alunos")
    tutor: Tutor = Relationship(back_populates="alunos")

class AlunoBaseWithTutor(AlunoBase):
    tutor: TutorBase
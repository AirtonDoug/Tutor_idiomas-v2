from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .turma import Turma
    from .aluno import Aluno

class TutorBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str

class Tutor(TutorBase, table=True):
    turmas: list['Turma'] = Relationship(back_populates="tutor")
    alunos: list['Aluno'] = Relationship(back_populates="tutor")
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .turma import Turma

class TutorBase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    lingua: str

class Tutor(TutorBase, table=True):
    turma: list['Turma'] = Relationship(back_populates="tutor")
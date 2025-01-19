from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turma import Turma

class AlunoBase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    

class Aluno(AlunoBase, table=True):
    turma_id: int | None = Field(default=None, foreign_key="turma.id")
    turma: 'Turma' = Relationship(back_populates="alunos")
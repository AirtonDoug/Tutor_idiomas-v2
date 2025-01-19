from sqlmodel import SQLModel, Field, Relationship
from .aluno import Aluno
from .tutor import Tutor

class TurmaBase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    nivel: str
    horario: str

class Turma(TurmaBase, table=True):
    tutor_id: int | None = Field(default=None, foreign_key="tutor.id")
    tutor: 'Tutor' = Relationship(back_populates="turmas")
    alunos: list['Aluno'] = Relationship(back_populates="turma")
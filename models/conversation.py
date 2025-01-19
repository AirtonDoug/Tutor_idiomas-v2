from datetime import datetime
from sqlmodel import SQLModel, Field


class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    data_horario: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
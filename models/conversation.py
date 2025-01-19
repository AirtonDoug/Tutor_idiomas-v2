from sqlmodel import SQLModel, Field, Relationship

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
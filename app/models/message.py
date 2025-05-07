# app/models/message.py
from datetime import datetime
from sqlmodel import Field, Relationship
from .base import Base

class Message(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    session_id: int = Field(foreign_key="session.id")
    session: "Session" = Relationship(back_populates="messages")

# app/models/session.py修改
from datetime import datetime
from sqlmodel import Field, Relationship
from .base import Base

class Session(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=3, max_length=30, regex=r"^[A-Za-z0-9]+$")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="sessions")
    
    messages: list["Message"] = Relationship(back_populates="session")
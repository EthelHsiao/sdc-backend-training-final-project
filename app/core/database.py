# app/core/database.py
from sqlmodel import SQLModel, create_engine, Session
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
engine = create_engine(DB_URL, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

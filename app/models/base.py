# app/models/base.py
from sqlmodel import SQLModel

class Base(SQLModel, table=True):
    __abstract__ = True

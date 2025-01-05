from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: int | None = Field(default=None, index=True)
    email: EmailStr = Field(default=None, unique=True, index=True)
    password: str | None = Field(default=None)
    test_field: str | None = Field(default=None)

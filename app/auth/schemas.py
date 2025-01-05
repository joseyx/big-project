from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: Optional[int] = Field(default=None, index=True)
    email: EmailStr = Field(default=None, unique=True, index=True)
    password: Optional[str] = Field(default=None)
    test_field: Optional[str] = Field(default=None)

class UserLogin(SQLModel):
    email: EmailStr
    password: str

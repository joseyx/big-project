from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: Optional[int] = Field(default=None, index=True)
    email: EmailStr = Field(default=None, unique=True, index=True)
    username: Optional[str] = Field(default=None, unique=True, index=True)
    password: Optional[str] = Field(default=None)

class PublicUser(SQLModel):
    id: Optional[int]
    name: str
    age: Optional[int]
    email: EmailStr
    username: Optional[str]

class Token(SQLModel):
    access_token: str
    message: str

class TokenData(SQLModel):
    username: str | None = None

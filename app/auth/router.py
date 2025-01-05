from typing import Annotated
from fastapi import APIRouter, Query
from sqlalchemy import select
from app.auth.schemas import User
from app.database import SessionDep

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/users", tags=["users"])
async def users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[User]:
    return session.exec(select(User).offset(offset).limit(limit)).all()
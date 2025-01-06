from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

# local imports
from app.auth.schemas import Token, User
from app.auth.utils import authenticate_user, get_user
from app.database import SessionDep
from app.config.oauth import create_access_token, hash_password


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/users", tags=["Users"])
async def users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[User]:
    return session.exec(select(User).offset(offset).limit(limit)).all()

# Auth routes
@router.post("/register", tags=["Auth"], status_code=HTTP_201_CREATED)
async def register(
    session: SessionDep,
    user_in: User,
):
    
    # Verify if the email already exists
    user = get_user(session, user_in.email)

    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Cipher the password
    hashed_password = hash_password(user_in.password)

    # Handle optinal username
    if not user_in.username:
        user_in.username = user_in.email

    # Create the user
    user = User(**user_in.model_dump(exclude={'password'}), password=hashed_password)

    # Add the user to the database
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User created successfully"
    }

@router.post("/login", tags=["Auth"], status_code=HTTP_200_OK)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
):
    
    # Construir la consulta para seleccionar el usuario por email
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data={
            "id": user.id,
            "username": user.username
        }
    )
    
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }
    request.session['is_logged'] = True

    return Token(access_token=access_token, message="Logged successfully")
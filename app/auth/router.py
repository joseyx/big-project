from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import select
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

# local imports
from app.auth.schemas import User, UserLogin
from app.database import SessionDep
from app.config.utils import hash_password, verify_password


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
    user = session.exec(select(User).where(User.email == user_in.email))

    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Cipher the password
    hashed_password = hash_password(user_in.password)

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
    user_login: UserLogin,
    request: Request,
):
    
    # Construir la consulta para seleccionar el usuario por email
    user = session.exec(select(User).where(User.email == user_login.email)).scalar_one_or_none()
    print(f"User: {user}")
    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    
    if not verify_password(user_login.password, user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User logged in successfully"
    }
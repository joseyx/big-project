import os
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.schemas import TokenData
from app.auth.utils import get_user
from app.config.oauth import ALGORITHM, oauth2_scheme
from app.database import SessionDep

async def get_current_user(session: SessionDep,token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code= HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        SECRET_TOKEN = os.getenv("TOKEN_SECRET")
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(session, username=token_data.username, include_password=False)
    if user is None:
        raise credentials_exception
    return user


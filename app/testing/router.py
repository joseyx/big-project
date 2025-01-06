from fastapi import APIRouter, Depends, Request
from typing import Annotated

from app.auth.dependencies import get_current_user
from app.auth.schemas import PublicUser, User

router = APIRouter(tags=["testing"])

@router.get("/test_session")
async def test_session(request: Request, current_user: Annotated[PublicUser, Depends(get_current_user)]):
    request.session['test'] = {
        'test': 'test',
        'name': 'Jose',
    }
    return {"message": "Session set", "current_user": current_user}

@router.get("/test_session_get")
async def test_session_get(request: Request):
    return request.session.get('test')

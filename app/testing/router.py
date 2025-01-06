from fastapi import APIRouter, Depends, Request
from typing import Annotated

from app.auth.dependencies import is_logged

router = APIRouter(tags=["testing"])

@router.get("/test_session")
async def test_session(request: Request, is_logged: Annotated[bool, Depends(is_logged)]):
    request.session['test'] = {
        'test': 'test',
        'name': 'Jose',
    }
    return {"message": "Session set"}

@router.get("/test_session_get")
async def test_session_get(request: Request):
    return request.session.get('test')

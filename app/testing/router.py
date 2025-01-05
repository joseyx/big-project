from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/test_session", tags=["users"])
async def test_session(request: Request):
    request.session['test'] = {
        'test': 'test',
        'name': 'Jose',
    }
    return {"message": "Session set"}

@router.get("/test_session_get", tags=["users"])
async def test_session_get(request: Request):
    return request.session.get('test')

from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

# TODO: replace with auth method like JWT or OAuth2
def is_logged(request: Request):
    if request.session.get('is_logged'):
        return True
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="User is not logged"
    )


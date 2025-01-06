from sqlalchemy import select
from sqlalchemy.orm import load_only

from app.auth.schemas import User
from app.config.oauth import verify_password


def get_user(session, username: str, include_password: bool = True):
    if include_password:
        user = session.exec(select(User).where(User.username == username)).scalar_one_or_none()
    else:
        user = session.exec(
            select(User)
            .where(User.username == username)
            .options(load_only(User.id, User.username, User.email))
        ).scalar_one_or_none()
        print(f"gotten user: {user}")
    return user
    
def authenticate_user(session, username: str, password: str):
    user:User = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
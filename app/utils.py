import bcrypt
from fastapi import HTTPException, status

from app.schemas import UserPublic
from app.config import SCOPES


def get_hashed_pwd(plain_pwd: str) -> bytes:
    pwd = plain_pwd.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt)


def verify_pwd(plain_pwd: str, hashed_pwd: bytes):
    pwd = plain_pwd.encode("utf-8")
    return bcrypt.checkpw(pwd, hashed_pwd)


def check_permission(user: UserPublic, required: str):
    if required not in SCOPES.get(user.user_type, {}):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights"
        )

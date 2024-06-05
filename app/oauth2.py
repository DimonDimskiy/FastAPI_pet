from datetime import datetime, timedelta


import jwt

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import UserPublic, Token


def create_token(data: UserPublic) -> Token:
    to_encode = data.model_dump()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return Token(access_token=access_token)

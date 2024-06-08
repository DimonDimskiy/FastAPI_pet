from datetime import datetime, timedelta

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import UserPublic, Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_token(data: UserPublic) -> Token:
    to_encode = data.model_dump()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return Token(access_token=access_token)


def verify_token(token: str = Depends(oauth2_scheme)) -> UserPublic:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return UserPublic(**payload)

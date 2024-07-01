from sqlmodel import Session
from fastapi import Header, HTTPException, status, Depends


from app.database import engine


def get_session():
    with Session(engine) as session:
        yield session


def get_language(lang: str = Header(default="en")):
    supported_languages = ["en", "ru"]
    if lang not in supported_languages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")
    return lang


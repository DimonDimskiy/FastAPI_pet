from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from app.dependencies import get_session



router = APIRouter(prefix="/programs", tags=["programs"])









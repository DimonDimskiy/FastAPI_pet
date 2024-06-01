from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from collections import defaultdict

from app.dependencies import get_session
from app.models import (
    Muscle,
    MuscleGroup,
    MuscleBase,
    MuscleGroupBase,
    ExerciseBase,
    Exercise,
)


router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[Exercise])
def get_exercises(session: Session = Depends(get_session)):
    raise NotImplementedError


@router.get("/by_group_id/{group_id}", response_model=list[Exercise])
def get_exercises_by_group_id(group_id: int, session: Session = Depends(get_session)):
    raise NotImplementedError


@router.get("/by_muscle_id/{muscle_id}", response_model=list[Exercise])
def get_exercises_by_muscle_id(muscle_id: int, session: Session = Depends(get_session)):
    raise NotImplementedError


@router.get("/latest/{n_latest}", response_model=list[Exercise])
def get_latest_exercises(n_latest: int, session: Session = Depends(get_session)):
    raise NotImplementedError


@router.get("/popular/{n_popular}", response_model=list[Exercise])
def get_popular_exercises(n_popular: int, session: Session = Depends(get_session)):
    raise NotImplementedError

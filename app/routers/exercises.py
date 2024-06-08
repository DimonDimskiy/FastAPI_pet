from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from app.dependencies import get_session
from app.models import Muscle, MuscleGroup, Exercise
from app.config import DEFAULT_LIMIT
from app.schemas import UserPublic
from app.utils import check_permission
from app.oauth2 import verify_token

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[Exercise])
def get_exercises(
    session: Session = Depends(get_session), limit: int = 10, offset: int = 0
):
    statement = select(Exercise).offset(offset).limit(limit)
    try:
        result = session.exec(statement).all()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no results for this request"
        )
    return result


@router.get(
    "/by_group_id/{group_id}",
)
def get_exercises_by_group_id(
    group_id: int,
    session: Session = Depends(get_session),
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
):
    statement = select(MuscleGroup).where(MuscleGroup.id == group_id)
    try:
        result = session.exec(statement).one().exercises[offset : offset + limit]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no results for this request"
        )
    return result


@router.get("/by_muscle_id/{muscle_id}", response_model=list[Exercise])
def get_exercises_by_muscle_id(
    muscle_id: int,
    session: Session = Depends(get_session),
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
):
    statement = select(Muscle).where(Muscle.id == muscle_id)
    try:
        result = session.exec(statement).one().exercises[offset : offset + limit]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no results for this request"
        )
    return result


@router.get("/latest", response_model=list[Exercise])
def get_latest_exercises(
    session: Session = Depends(get_session), limit: int = DEFAULT_LIMIT, offset: int = 0
):
    statement = (
        select(Exercise).order_by(Exercise.created_at).offset(offset).limit(limit)
    )

    try:
        result = session.exec(statement).all()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no results for this request"
        )

    return result


@router.get("/popular", response_model=list[Exercise])
def get_popular_exercises(
    session: Session = Depends(get_session),
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/", response_model=Exercise)
def create_exercise(session: Session = Depends(get_session),
                    user: UserPublic = Depends(verify_token)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/", response_model=Exercise)
def update_exercise(session: Session = Depends(get_session),
                    user: UserPublic = Depends(verify_token)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
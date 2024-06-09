from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlmodel import Session, select, col
from sqlalchemy.exc import NoResultFound

from app.dependencies import get_session
from app.models import Muscle, MuscleGroup, Exercise
from app.config import DEFAULT_LIMIT
from app.schemas import ExerciseCreate, UserPublic, ExercisePublic
from app.utils import check_permission
from app.oauth2 import verify_token

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExercisePublic])
def get_exercises(
    session: Session = Depends(get_session),
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    search: str = "",
):
    statement = (
        select(Exercise)
        .where(col(Exercise.name).contains(search))
        .offset(offset)
        .limit(limit)
    )
    try:
        result = session.exec(statement).all()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no results for this request"
        )
    return result


@router.get("/by_group_id/{group_id}", response_model=list[ExercisePublic])
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


@router.get("/by_muscle_id/{muscle_id}", response_model=list[ExercisePublic])
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


@router.get("/latest", response_model=list[ExercisePublic])
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


@router.post("/", response_model=ExercisePublic, status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise: ExerciseCreate,
    session: Session = Depends(get_session),
    user: UserPublic = Depends(verify_token),
):
    try:
        exercise.muscle_groups = session.exec(
            select(MuscleGroup).where(col(MuscleGroup.id).in_(exercise.muscle_groups))
        ).all()
        exercise.muscles = session.exec(
            select(Muscle).where(col(Muscle.id).in_(exercise.muscles))
        ).all()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect muscle_group or muscle id",
        )

    db_exercise = Exercise.model_validate(exercise, update={"created_by": user.id})
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return db_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(
    exercise_id: int,
    session: Session = Depends(get_session),
    user: UserPublic = Depends(verify_token),
):
    try:
        exercise = session.exec(
            select(Exercise).where(Exercise.id == exercise_id)
        ).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id:{exercise_id} was not found",
        )

    if exercise.created_by != user.id:
        check_permission(user, "exercise_delete")

    session.delete(exercise)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=ExercisePublic)
def update_exercise(
    session: Session = Depends(get_session), user: UserPublic = Depends(verify_token)
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/popular", response_model=list[ExercisePublic])
def get_popular_exercises(
    session: Session = Depends(get_session),
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)

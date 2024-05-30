from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from app.dependencies import get_session
from app.models import Muscle, MuscleGroup, MuscleBase, MuscleGroupBase


router = APIRouter(
    prefix="/muscles",
    tags=["muscles"]
)


@router.get("/groups", response_model=list[MuscleGroup])
def get_muscle_groups(session: Session = Depends(get_session)):
    muscle_groups = session.exec(select(MuscleGroup)).all()
    if not muscle_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"there is no groups yet")
    return muscle_groups


@router.get("/groups/{id}", response_model=MuscleGroup)
def get_muscle_group_by_id(muscle_group_id: int,
                           session: Session = Depends(get_session)):
    statement = select(MuscleGroup).where(MuscleGroup.id == muscle_group_id)
    try:
        muscle_group = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"muscle_group with id: {muscle_group_id} was not found")
    return muscle_group


@router.post("/groups",
             status_code=status.HTTP_201_CREATED,
             response_model=MuscleGroup)
def create_muscle_group(group: MuscleGroupBase,
                        session: Session = Depends(get_session)):
    db_muscle_group = MuscleGroup.model_validate(group)
    session.add(db_muscle_group)
    session.commit()
    session.refresh(db_muscle_group)
    return db_muscle_group


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=Muscle)
def create_muscle(muscle: MuscleBase,
                  session: Session = Depends(get_session)):
    db_muscle = Muscle.model_validate(muscle)
    session.add(db_muscle)
    session.commit()
    session.refresh(db_muscle)
    return db_muscle


@router.get("/", response_model=list[Muscle])
def get_muscles(session: Session = Depends(get_session)):
    muscles = session.exec(select(Muscle)).all()
    if not muscles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"there is no muscles yet")
    return muscles


@router.get("/{muscle_id}", response_model=Muscle)
def get_muscle_by_id(muscle_id: int,
                     session: Session = Depends(get_session)):
    statement = select(Muscle).where(muscle_id == Muscle.id)
    try:
        muscle = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"muscle with id: {muscle_id} was not found")
    return muscle


@router.delete("/{muscle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_muscle(muscle_id: int,
                  session: Session = Depends(get_session)):
    statement = select(Muscle).where(Muscle.id == muscle_id)
    try:
        muscle = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"muscle with id: {muscle_id} was not found")
    session.delete(muscle)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



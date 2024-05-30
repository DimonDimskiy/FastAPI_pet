from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from app.dependencies import get_session
from app.models import Program


router = APIRouter(
    prefix="/programs",
    tags=["programs"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_program(program: Program, session: Session = Depends(get_session)):
    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@router.get("/")
def get_programs(session: Session = Depends(get_session)):
    programs = session.exec(select(Program)).all()
    if programs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"there is no programs yet")
    return programs


@router.get("/{program_id}")
def get_program_by_id(program_id: int, session: Session = Depends(get_session)):
    statement = select(Program).where(Program.id == program_id)
    try:
        program = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"program with id: {program_id} was not found")
    return program


@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: int, session: Session = Depends(get_session)):
    statement = select(Program).where(Program.id == program_id)
    try:
        program = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"program with id: {program_id} was not found")
    session.delete(program)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

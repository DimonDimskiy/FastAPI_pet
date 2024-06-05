from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.dependencies import get_session
from app.schemas import UserCreate, UserPublic
from app.models import User
from app.utils import get_hashed_pwd, verify_pwd
from app.oauth2 import create_token

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_none(email: str, session: Session) -> User | None:
    statement = select(User).where(email == User.email)
    return session.exec(statement).one_or_none()


@router.post("/new",
             status_code=status.HTTP_201_CREATED,
             response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    if get_user_or_none(user.email, session) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email {user.email} already exist")
    user.password = get_hashed_pwd(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)):
    user = get_user_or_none(user_credentials.username, session)
    if user is None or not verify_pwd(
            user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    public_user = UserPublic.model_validate(user)
    token = create_token(public_user)
    return token

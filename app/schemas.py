from datetime import datetime

from sqlmodel import Field, SQLModel, AutoString
from pydantic import EmailStr


class MuscleBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str | None = Field()
    large_image: str | None = Field()
    group_id: int = Field(nullable=False, foreign_key="muscle_group.id", index=True)


class MuscleGroupBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = Field()
    image: str = Field()


class ExerciseBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str = Field(nullable=False)
    video: str | None = Field()


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)


class UserCreate(UserBase):
    password: str = Field(nullable=False)


class UserPublic(UserBase):
    id: int
    user_type: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

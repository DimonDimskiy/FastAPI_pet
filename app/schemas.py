from sqlmodel import Field, SQLModel, AutoString
from pydantic import EmailStr


class MuscleBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str | None = Field()
    large_image: str | None = Field()
    group_id: int = Field(nullable=False, foreign_key="muscle_group.id", index=True)


class MusclePublic(MuscleBase):
    id: int


class MuscleGroupBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None = Field()
    image: str = Field()


class MuscleGroupPublic(MuscleGroupBase):
    id: int


class ExerciseBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str = Field(nullable=False)
    video: str | None = Field()


class ExerciseCreate(ExerciseBase):
    muscle_groups: list[int]
    muscles: list[int]


class ExercisePublic(ExerciseBase):
    id: int
    created_by: int
    muscle_groups: list[MuscleGroupPublic]
    muscles: list[MusclePublic]


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

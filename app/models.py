from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship

from .schemas import MuscleBase, MuscleGroupBase, ExerciseBase, UserBase


class ExerciseGroupLink(SQLModel, table=True):
    group_id: int | None = Field(
        default=None, primary_key=True, foreign_key="muscle_group.id"
    )
    exercise_id: int | None = Field(
        default=None, primary_key=True, foreign_key="exercise.id"
    )


class ExerciseMuscleLink(SQLModel, table=True):
    muscle_id: int | None = Field(
        default=None, primary_key=True, foreign_key="muscle.id"
    )
    exercise_id: int | None = Field(
        default=None, primary_key=True, foreign_key="exercise.id"
    )


class MuscleGroup(MuscleGroupBase, table=True):
    __tablename__ = "muscle_group"

    exercises: list["Exercise"] = Relationship(
        back_populates="muscle_groups", link_model=ExerciseGroupLink
    )


class Muscle(MuscleBase, table=True):
    __tablename__ = "muscle"

    exercises: list["Exercise"] = Relationship(
        back_populates="muscles", link_model=ExerciseMuscleLink
    )


class Exercise(ExerciseBase, table=True):
    __tablename__ = "exercise"

    created_by: str | None = Field()
    created_at: datetime = Field(default_factory=datetime.now)

    muscle_groups: list[MuscleGroup] = Relationship(
        back_populates="exercises", link_model=ExerciseGroupLink
    )
    muscles: list[Muscle] = Relationship(
        back_populates="exercises", link_model=ExerciseMuscleLink
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    password: bytes = Field()
    user_type: str | None = Field(default="basic")

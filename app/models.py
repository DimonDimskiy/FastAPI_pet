from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship


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


class MuscleBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str | None = Field()
    large_image: str | None = Field()
    group_id: int = Field(nullable=False, foreign_key="muscle_group.id", index=True)


class MuscleGroupBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None = Field()
    image: str = Field()


class MuscleGroup(MuscleGroupBase, table=True):
    __tablename__ = "muscle_group"

    id: int | None = Field(default=None, primary_key=True)

    exercises: list["Exercise"] = Relationship(
        back_populates="muscle_groups", link_model=ExerciseGroupLink
    )


class Muscle(MuscleBase, table=True):
    __tablename__ = "muscle"

    id: int | None = Field(default=None, primary_key=True)
    exercises: list["Exercise"] = Relationship(
        back_populates="muscles", link_model=ExerciseMuscleLink
    )


class ExerciseBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str = Field(nullable=False)
    video: str | None = Field()


class Exercise(ExerciseBase, table=True):
    __tablename__ = "exercise"

    id: int | None = Field(default=None, primary_key=True)

    created_by: str | None = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    votes: int | None = Field(default=0)

    muscle_groups: list[MuscleGroup] = Relationship(
        back_populates="exercises", link_model=ExerciseGroupLink
    )
    muscles: list[Muscle] = Relationship(
        back_populates="exercises", link_model=ExerciseMuscleLink
    )

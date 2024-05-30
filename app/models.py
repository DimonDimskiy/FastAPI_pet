from sqlmodel import Field, SQLModel


class MuscleBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str | None = Field()
    group_id: int = Field(nullable=False, foreign_key="muscle_groups.id")


class MuscleGroupBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str = Field()


class MuscleGroup(MuscleGroupBase,  table=True):
    __tablename__ = "muscle_groups"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str = Field()


class Muscle(MuscleBase, table=True):
    __tablename__ = "muscles"

    id: int | None = Field(default=None, primary_key=True)


class Program(SQLModel, table=True):
    __tablename__ = "program"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    brief: str = Field()








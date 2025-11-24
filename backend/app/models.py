import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Column
from sqlalchemy.dialects.postgresql import JSONB


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    workouts: list["Workout"] | None = Relationship(back_populates="owner", cascade_delete=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
# Shared properties
class WorkoutBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to receive on item creation
class WorkoutCreate(WorkoutBase):
    exercises: dict = Field(sa_column=Column(JSONB))

# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Properties to receive on item update
class WorkoutUpdate(WorkoutBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")

# Link table for many to many relationship    
#class ExerciseWorkoutLink(SQLModel, table=True):
#    exercise_id: uuid.UUID | None = Field(default=None, foreign_key="exercise.id", primary_key=True) 
#    workout_id: uuid.UUID | None = Field(default=None, foreign_key="workout.id", primary_key=True) 
    
# Database model, database table inferred from class name
class Workout(WorkoutBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="workouts")
    #exercises: list["Exercise"] = Relationship(back_populates="workouts", link_model=ExerciseWorkoutLink)
    exercises: dict = Field(sa_column=Column(JSONB))

# Database model for exercises
class ExerciseBase(SQLModel):
    #id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=255)

class Exercise(ExerciseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #workout_id: uuid.UUID =Field(default=uuid.uuid4, foreign_key="workout.id")
    #workouts: list[Workout] = Relationship(back_populates="exercises", link_model = ExerciseWorkoutLink)
    
    
class ExerciseCreate(ExerciseBase):
    pass

# Properties to receive on item update
class ExerciseUpdate(ExerciseBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    
# Properties to return via API, id is always required
class ExercisePublic(ExerciseBase):
    id: uuid.UUID
    
class ExercisesPublic(SQLModel):
    data: list[ExercisePublic]
    count: int

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID

# Properties to return via API, id is always required
class WorkoutPublic(WorkoutBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    exercises: dict = Field(sa_column=Column(JSONB))

class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int

class WorkoutsPublic(SQLModel):
    data: list[WorkoutPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

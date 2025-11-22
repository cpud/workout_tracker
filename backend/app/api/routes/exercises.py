import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Exercise, ExerciseCreate, ExercisePublic, ExercisesPublic, ExerciseUpdate, Message

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=ExercisesPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve exercises.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Exercise)
        count = session.exec(count_statement).one()
        statement = select(Exercise).offset(skip).limit(limit)
        exercises = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Exercise)
            #.where(Item.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Exercise)
            #.where(Item.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        exercises = session.exec(statement).all()

    return ExercisesPublic(data=exercises, count=count)


@router.get("/{id}", response_model=ExercisePublic)
def read_exercise(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get exercise by ID.
    """
    exercise = session.get(Exercise, id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Item not found")
    #if not current_user.is_superuser and (item.owner_id != current_user.id):
    #    raise HTTPException(status_code=400, detail="Not enough permissions")
    return exercise


@router.post("/", response_model=ExercisePublic)
def create_exercise(
    *, session: SessionDep, exercise_in: ExerciseCreate
) -> Any:
    """
    Create new exercise.
    """
    exercise = Exercise.model_validate(exercise_in)
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


@router.put("/{id}", response_model=ExercisePublic)
def update_item(
    *,
    session: SessionDep,
    #current_user: CurrentUser,
    id: uuid.UUID,
    exercise_in: ExerciseUpdate,
) -> Any:
    """
    Update an exercise.
    """
    exercise = session.get(Exercise, id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    #if not current_user.is_superuser and (item.owner_id != current_user.id):
    #    raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = exercise_in.model_dump(exclude_unset=True)
    exercise.sqlmodel_update(update_dict)
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


#@router.delete("/{id}")
#def delete_item(
#    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
#) -> Message:
#    """
#    Delete an item.
#    """
#    item = session.get(Item, id)
#    if not item:
#        raise HTTPException(status_code=404, detail="Item not found")
#    if not current_user.is_superuser and (item.owner_id != current_user.id):
#        raise HTTPException(status_code=400, detail="Not enough permissions")
#    session.delete(item)
#    session.commit()
#    return Message(message="Item deleted successfully")

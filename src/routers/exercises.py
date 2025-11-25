from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.models.exercise import Exercise
from src.schemas.exercise import ExerciseOut

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseOut])
async def get_all_exercises(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Exercise).order_by(Exercise.name))
    exercises = result.scalars().all()

    return [ExerciseOut.model_validate(ex) for ex in exercises]

@router.get("/{exercise_id}", response_model=ExerciseOut)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")

    return ExerciseOut.model_validate(exercise)
from sqlalchemy import select
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.models.diary import Diary
from src.models.exercise import Exercise
from src.dependencies.auth import get_current_user
from src.models.training import Training, TrainingExercise
from src.schemas.training import TrainingCreate, TrainingOut


router = APIRouter(prefix="/trainings", tags=["trainings"])


async def _get_my_diary(user: dict, db: AsyncSession) -> Diary:
    stmt = select(Diary).where(
        Diary.trainer_id == user["id"]
        if user["role"] == "trainer"
        else Diary.client_id == user["id"]
    )
    result = await db.execute(stmt)
    diary = result.scalar_one_or_none()
    if not diary:
        raise HTTPException(status_code=404, detail="Дневник не найден")
    return diary


@router.get("/", response_model=list[TrainingOut])
async def get_trainings(
    dt: date | None = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    diary = await _get_my_diary(current_user, db)

    stmt = select(Training).where(Training.diary_id == diary.id)

    if dt is not None:
        stmt = stmt.where(Training.date == dt)

    stmt = stmt.order_by(Training.date.desc(), Training.id)

    result = await db.execute(stmt)
    trainings = result.scalars().all()

    return [TrainingOut.model_validate(t) for t in trainings]


@router.post("/", response_model=TrainingOut, status_code=201)
async def create_training(
    payload: TrainingCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "trainer":
        raise HTTPException(status_code=403,
                            detail="Только тренер может создавать тренировки")

    diary = await _get_my_diary(current_user, db)

    if payload.diary_id != diary.id:
        raise HTTPException(status_code=403,
                            detail="Нельзя создавать"
                                   " тренировку в чужом дневнике")

    if payload.exercises:
        exercise_ids = [ex.exercise_id for ex in payload.exercises]
        result = await db.execute(
            select(Exercise.id).where(Exercise.id.in_(exercise_ids))
        )
        found_ids = {row[0] for row in result.fetchall()}
        if missing := set(exercise_ids) - found_ids:
            raise HTTPException(status_code=404,
                                detail=f"Упражнения не найдены: {missing}")

    training = Training(
        diary_id=diary.id,
        name=payload.name,
        date=payload.date,
        start_at=payload.start_at,
        end_at=payload.end_at,
    )
    db.add(training)
    await db.commit()
    await db.refresh(training)

    for ex in payload.exercises:
        te = TrainingExercise(
            training_id=training.id,
            exercise_id=ex.exercise_id,
            order_index=ex.order_index,
            sets_count=ex.sets_count,
            set_duration=ex.set_duration,
            weight=ex.weight,
        )
        db.add(te)

    await db.commit()
    await db.refresh(training)
    return TrainingOut.model_validate(training)


@router.patch("/{training_id}/start", response_model=TrainingOut)
async def start_training(
    training_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Клиент начинает тренировку"""
    if current_user["role"] != "client":
        raise HTTPException(status_code=403,
                            detail="Только клиент может начать тренировку")

    diary = await _get_my_diary(current_user, db)
    training = await db.get(Training, training_id)

    if not training:
        raise HTTPException(status_code=404,
                            detail="Тренировка не найдена")
    if training.diary_id != diary.id:
        raise HTTPException(status_code=403,
                            detail="Это не ваша тренировка")
    if training.start_at is not None:
        raise HTTPException(status_code=400,
                            detail="Тренировка уже начата")

    training.start_at = datetime.utcnow()
    await db.commit()
    await db.refresh(training)
    return TrainingOut.model_validate(training)


@router.patch("/{training_id}/finish", response_model=TrainingOut)
async def finish_training(
    training_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403,
                            detail="Только клиент может завершить тренировку")

    diary = await _get_my_diary(current_user, db)
    training = await db.get(Training, training_id)

    if not training:
        raise HTTPException(status_code=404,
                            detail="Тренировка не найдена")
    if training.diary_id != diary.id:
        raise HTTPException(status_code=403,
                            detail="Это не ваша тренировка")
    if training.start_at is None:
        raise HTTPException(status_code=400,
                            detail="Тренировка ещё не начата")
    if training.end_at is not None:
        raise HTTPException(status_code=400,
                            detail="Тренировка уже завершена")

    training.end_at = datetime.utcnow()
    await db.commit()
    await db.refresh(training)

    return TrainingOut.model_validate(training)


@router.delete("/{training_id}", status_code=204)
async def delete_training(
    training_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "trainer":
        raise HTTPException(status_code=403,
                            detail="Только тренер может удалять тренировки")

    diary = await _get_my_diary(current_user, db)
    training = await db.get(Training, training_id)

    if not training:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    if training.diary_id != diary.id:
        raise HTTPException(status_code=403, detail="Это не ваша тренировка")

    await db.delete(training)
    await db.commit()

    return None
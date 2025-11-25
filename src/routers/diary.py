from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.models.diary import Diary
from src.schemas.diary import DiaryOut, DiaryJoin
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/diary", tags=["diary"])


@router.get("/", response_model=DiaryOut)
async def get_my_diary(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] == "trainer":
        result = await db.execute(
            select(Diary).where(Diary.trainer_id == current_user["id"])
        )
    else:
        result = await db.execute(
            select(Diary).where(Diary.client_id == current_user["id"])
        )

    diary = result.scalar_one_or_none()
    if not diary:
        raise HTTPException(status_code=404, detail="Дневник не найден")

    return DiaryOut.model_validate(diary)


@router.post("/", response_model=DiaryOut, status_code=201)
async def create_diary(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "trainer":
        raise HTTPException(status_code=403,
                            detail="Только тренер может создать дневник")

    exists = await db.execute(select(Diary).where(
        Diary.trainer_id == current_user["id"])
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="У вас уже есть дневник")

    diary = Diary(
        name="Мой дневник",
        trainer_id=current_user["id"],
        client_id=None,
    )
    db.add(diary)
    await db.commit()
    await db.refresh(diary)

    return DiaryOut.model_validate(diary)


@router.post("/join", response_model=DiaryOut)
async def join_diary(
    payload: DiaryJoin,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403,
                            detail="Только клиент может присоединиться")

    has_diary = await db.execute(
        select(Diary).where(Diary.client_id == current_user["id"])
    )
    if has_diary.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Вы уже в дневнике")

    diary = await db.get(Diary, payload.diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Дневник не найден")
    if diary.client_id is not None:
        raise HTTPException(status_code=400, detail="Место уже занято")

    diary.client_id = current_user["id"]
    await db.commit()
    await db.refresh(diary)
    return DiaryOut.model_validate(diary)


@router.delete("/", status_code=204)
async def delete_diary(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user["role"] != "trainer":
        raise HTTPException(status_code=403,
                            detail="Только тренер может удалить дневник")

    result = await db.execute(
        select(Diary).where(Diary.trainer_id == current_user["id"])
    )
    diary = result.scalar_one_or_none()
    if not diary:
        raise HTTPException(status_code=404, detail="Дневник не найден")

    await db.delete(diary)
    await db.commit()

    return None
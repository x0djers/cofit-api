from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.models.user import User
from src.db.session import get_db
from src.core.security import (get_password_hash,
                               verify_password,
                               create_access_token)
from src.schemas.user import UserCreate, UserOut, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",
             response_model=UserOut,
             status_code=HTTPStatus.CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        first_name=user_in.first_name,
        second_name=user_in.second_name,
        email=str(user_in.email),
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserOut.model_validate(user)

@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token({"sub": str(user.id)})

    return Token(access_token=access_token)

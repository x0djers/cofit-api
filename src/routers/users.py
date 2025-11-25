from fastapi import APIRouter, Depends

from src.schemas.user import UserOut
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def read_me(current_user: dict = Depends(get_current_user)):
    return UserOut.model_validate(current_user)
from typing import Literal

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: str
    role: Literal["client", "trainer"]


class UserOut(BaseModel):
    id: int
    first_name: str
    second_name: str
    email: EmailStr
    role: Literal["client", "trainer"]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
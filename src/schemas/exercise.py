from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    description: str | None = None
    is_weight: bool = False
    is_duration: bool = False

class ExerciseOut(ExerciseBase):
    id: int

    class Config:
        from_attributes = True

from datetime import date, datetime

from pydantic import BaseModel

class TrainingExerciseBase(BaseModel):
    exercise_id: int
    order_index: int
    sets_count: int
    set_duration: int | None = None
    weight: float | None = None

class TrainingExerciseCreate(TrainingExerciseBase):
    pass

class TrainingExerciseOut(TrainingExerciseBase):
    id: int

    class Config:
        from_attributes = True

class TrainingBase(BaseModel):
    name: str
    date: date
    start_at: datetime | None = None
    end_at: datetime | None = None

class TrainingCreate(TrainingBase):
    diary_id: int
    exercises: list[TrainingExerciseCreate] = []

class TrainingOut(TrainingBase):
    id: int
    diary_id: int
    exercises: list[TrainingExerciseOut] = []

    class Config:
        from_attributes = True
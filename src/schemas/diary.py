from pydantic import BaseModel

class DiaryBase(BaseModel):
    name: str

class DiaryCreate(DiaryBase):
    trainer_id: int

class DiaryOut(DiaryBase):
    id: int
    trainer_id: int
    client_id: int

    class Config:
        from_attributes = True
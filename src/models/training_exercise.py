from sqlalchemy.types import Numeric
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index

from src.db.base import Base

class TrainingExercise(Base):
    __tablename__ = "training_exercises"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order_index = Column(Integer, default=0)
    sets_count = Column(Integer, nullable=False)
    set_duration = Column(Integer)
    weight = Column(Numeric(6, 2))

    __table_args__ = (
        UniqueConstraint("training_id",
                         "exercise_id",
                         name="uq_training_exercise"),
        Index("ix_training_order", "training_id", "order_index"),
    )
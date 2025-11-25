from sqlalchemy import (Column,
                        Integer,
                        String,
                        Date,
                        ForeignKey,
                        Index,
                        Numeric,
                        TIMESTAMP,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from src.db.base import Base

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer,
                      ForeignKey("diarys.id"),
                      nullable=False,
                      index=True)
    name = Column(String(100), nullable=False, default="Тренировка")
    date = Column(Date, nullable=False)
    start_at = Column(TIMESTAMP(timezone=True), nullable=True)
    end_at = Column(TIMESTAMP(timezone=True), nullable=True)

    diary = relationship("Diary", backref="trainings")
    exercises = relationship(
        "TrainingExercise",
        back_populates="training",
        cascade="all, delete-orphan",
        order_by="TrainingExercise.order_index"
    )

    __table_args__ = (
        Index("ix_training_diary_date", "diary_id", "date"),
    )


class TrainingExercise(Base):
    __tablename__ = "training_exercises"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order_index = Column(Integer, default=0)
    sets_count = Column(Integer, nullable=False)
    set_duration = Column(Integer, nullable=True)
    weight = Column(Numeric(6, 2), nullable=True)

    training = relationship("Training", back_populates="exercises")
    exercise = relationship("Exercise")

    __table_args__ = (
        UniqueConstraint("training_id", "exercise_id",
                         name="uq_training_exercise"),
        Index("ix_training_order", "training_id", "order_index"),
    )

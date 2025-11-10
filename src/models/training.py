from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index

from src.core.db.base import Base

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer,
                      ForeignKey("diarys.id"),
                      nullable=False,
                      index=True)
    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    start_at = Column(TIMESTAMP, unique=True)
    end_at = Column(TIMESTAMP, unique=True)

    __table_args__ = (
        Index("ix_training_diary_date",
              "diary_id",
              "date"),
    )
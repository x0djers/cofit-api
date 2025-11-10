from sqlalchemy import Column, Integer, String, Text, Boolean

from src.core.db.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    is_weight = Column(Boolean, default=False)
    is_duration = Column(Boolean, default=False)
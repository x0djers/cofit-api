from sqlalchemy import Column, Integer, String, Date, ForeignKey, func

from src.db.base import Base

class Diary(Base):
    __tablename__ = "diarys"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date, server_default=func.current_date(),
                        nullable=False)
    name = Column(String(100), nullable=False)
    trainer_id = Column(Integer,
                        ForeignKey("users.id"),
                        nullable=False,
                        unique=True)
    client_id: int | None = Column(Integer,
                                   ForeignKey("users.id"),
                                   nullable=True,
                                   unique=True)
from sqlalchemy import Column, Integer, String, Date, Enum, func

from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        Date,
        server_default=func.current_date(),
        nullable=False
    )
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("client", "trainer", name="user_role"),
                  nullable=False,
                  index=True)
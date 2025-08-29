import datetime
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP

from database.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="USER")
    adult_content = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

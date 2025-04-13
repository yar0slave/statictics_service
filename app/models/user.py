from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
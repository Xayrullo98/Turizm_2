from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, func
from sqlalchemy.orm import relationship

from db import Base


class Gids(Base):
    __tablename__ = "Gids"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    phone = Column(String(30), nullable=False)
    address = Column(String(50),  nullable=True)
    languages = Column(String(200), nullable=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

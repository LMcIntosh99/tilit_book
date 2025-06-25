from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())

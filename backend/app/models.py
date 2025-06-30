"""
SQLAlchemy model defining the Comment table structure in the database.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base


class Comment(Base):
    """
    Represents a comment left by a user.

    Attributes:
        id (int): Primary key, auto-incrementing comment ID.
        text (str): The content of the comment.
        location (str): Location associated with the comment.
        created_at (datetime): Timestamp when the comment was created.
        image_url (str, optional): URL of an optional image attached to the comment.
    """
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    image_url = Column(String, nullable=True)

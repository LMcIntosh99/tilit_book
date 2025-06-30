"""
Pydantic schemas for validating and serializing Comment data.

Includes schemas for creating comments and returning comment data.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentCreate(BaseModel):
    """
    Schema for creating a new comment.

    Attributes:
        text (str): The content of the comment.
        location (str): The location associated with the comment.
        image_url (Optional[str]): Optional URL of an image attached to the comment.
    """
    text: str
    location: str
    image_url: Optional[str]


class Comment(BaseModel):
    """
    Schema representing a comment as stored and retrieved from the database.

    Attributes:
        id (int): Unique identifier for the comment.
        text (str): The content of the comment.
        location (str): The location associated with the comment.
        created_at (datetime): Timestamp of when the comment was created.
        image_url (Optional[str]): Optional URL of an image attached to the comment.
    """
    id: int
    text: str
    location: str
    created_at: datetime
    image_url: Optional[str]

    class Config:
        """
        Tells Pydantic to allow model creation from SQLAlchemy models.
        """
        from_attributes = True

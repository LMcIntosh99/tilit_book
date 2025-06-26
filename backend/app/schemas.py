from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    text: str
    location: str
    image_url: Optional[str] = None


class Comment(BaseModel):
    id: int
    text: str
    location: str
    created_at: datetime
    image_url: Optional[str]

    class Config:
        from_attributes = True

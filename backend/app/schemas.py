from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    text: str
    location: str
    image_key: Optional[str]


class Comment(BaseModel):
    id: int
    text: str
    location: str
    created_at: datetime
    image_key: Optional[str]

    class Config:
        from_attributes = True

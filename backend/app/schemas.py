from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, File


class CommentCreate(BaseModel):
    text: str
    location: str
    image_url: Optional[str]


class Comment(BaseModel):
    id: int
    text: str
    location: str
    created_at: datetime
    image_url: Optional[str]

    class Config:
        from_attributes = True

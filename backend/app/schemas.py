from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    text: str
    location: str

class Comment(BaseModel):
    id: int
    text: str
    location: str
    created_at: datetime

    class Config:
        orm_mode = True

from fastapi import APIRouter, Depends, Form, File, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas
import uuid
from ..utils.logger import logger

router = APIRouter()

BUCKET = "tilit-imgs"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/comments", response_model=list[schemas.Comment])
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments(db)


@router.post("/comments", response_model=schemas.Comment)
def create_comment(
        text: str = Form(...),
        location: str = Form(...),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    logger.info("POST comments")
    image_url = None

    if file:
        file_ext = file.filename.split(".")[-1]
        key = f"cat-images/{uuid.uuid4()}.{file_ext}"
        image_url = f"https://{BUCKET}.s3.amazonaws.com/{key}"
    logger.info(image_url)
    return crud.create_comment(db, schemas.CommentCreate(text=text, location=location, image_url=image_url), image_url)

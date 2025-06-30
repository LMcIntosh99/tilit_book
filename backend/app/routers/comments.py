from fastapi import APIRouter, Depends, Form, File, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas
import uuid
from ..utils.s3_tools import upload_image
from ..utils.logger import logger

router = APIRouter()


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
    image_key = None

    if file:
        image_key = upload_image(file)

    logger.info(image_key)
    return crud.create_comment(db, schemas.CommentCreate(text=text, location=location, image_key=image_key))

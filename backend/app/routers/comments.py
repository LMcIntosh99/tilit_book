"""
FastAPI router for handling comment-related API endpoints.

Includes endpoints to:
- Retrieve all comments.
- Create a new comment, optionally uploading an image to S3.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas
from ..utils.s3_tools import upload_image

router = APIRouter()


def get_db():
    """
    Provide a database session to path operation functions.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/comments", response_model=list[schemas.Comment])
def read_comments(db: Session = Depends(get_db)):
    """
    Retrieve all comments from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[schemas.Comment]: List of Comment objects.
    """
    return crud.get_comments(db)


@router.post("/comments", response_model=schemas.Comment)
def create_comment(
        text: str = Form(...),
        location: str = Form(...),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    """
    Create a new comment with optional image upload.

    Args:
        text (str): The comment text, submitted via form.
        location (str): Location associated with the comment, via form.
        file (Optional[UploadFile]): Optional image file uploaded.
        db (Session): Database session dependency.

    Returns:
        schemas.Comment: The newly created Comment object.
    """
    image_url = None

    if file:
        image_url = upload_image(file)

    return crud.create_comment(
        db,
        schemas.CommentCreate(text=text, location=location, image_url=image_url)
    )

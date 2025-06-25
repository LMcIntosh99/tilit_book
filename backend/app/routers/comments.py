from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

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
def post_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment)

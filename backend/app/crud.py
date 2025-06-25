from sqlalchemy.orm import Session
from . import models, schemas

def get_comments(db: Session):
    return db.query(models.Comment).order_by(models.Comment.created_at.desc()).all()

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

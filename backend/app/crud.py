"""
This module provides CRUD operations related to comments in the database.

Functions:
- get_comments: Fetches all comments ordered by creation date (newest first).
- create_comment: Creates and saves a new comment record.
"""

from sqlalchemy.orm import Session
from . import models, schemas


def get_comments(db: Session):
    """
    Retrieve all comments from the database.

    Args:
        db (Session): Database session for querying.

    Returns:
        List[models.Comment]: List of Comment objects ordered by most recent first.
    """
    return db.query(models.Comment).order_by(models.Comment.created_at.desc()).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    """
    Create a new comment record in the database.

    Args:
        db (Session): Database session for committing the new comment.
        comment (schemas.CommentCreate): Data transfer object containing comment details.

    Returns:
        models.Comment: The newly created Comment object, refreshed from the DB.
    """
    db_comment = models.Comment(
        text=comment.text,
        location=comment.location,
        image_url=comment.image_url
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

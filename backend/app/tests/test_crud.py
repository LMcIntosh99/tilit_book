"""
Unit tests for CRUD operations.

These tests use PostgreSQL (same as production) to ensure database compatibility.
Falls back to SQLite for local development if PostgreSQL is not available.
"""

import pytest
from datetime import datetime

from ..models import Comment
from ..schemas import CommentCreate
from .. import crud


def test_create_comment(db_session):
    """Test creating a comment."""
    comment_data = CommentCreate(
        text="Test comment",
        location="Test location",
        image_url="https://example.com/image.jpg"
    )

    created_comment = crud.create_comment(db_session, comment_data)

    assert created_comment.id is not None
    assert created_comment.text == "Test comment"
    assert created_comment.location == "Test location"
    assert created_comment.image_url == "https://example.com/image.jpg"
    assert isinstance(created_comment.created_at, datetime)


def test_create_comment_without_image(db_session):
    """Test creating a comment without an image URL."""
    comment_data = CommentCreate(
        text="Test comment without image",
        location="Test location",
        image_url=None
    )

    created_comment = crud.create_comment(db_session, comment_data)

    assert created_comment.id is not None
    assert created_comment.text == "Test comment without image"
    assert created_comment.location == "Test location"
    assert created_comment.image_url is None
    assert isinstance(created_comment.created_at, datetime)


def test_get_comments_empty(db_session):
    """Test getting comments when database is empty."""
    comments = crud.get_comments(db_session)
    assert comments == []


def test_get_comments_single(db_session):
    """Test getting comments with a single comment."""
    comment_data = CommentCreate(
        text="Single comment",
        location="Single location",
        image_url=None
    )

    crud.create_comment(db_session, comment_data)
    comments = crud.get_comments(db_session)

    assert len(comments) == 1
    assert comments[0].text == "Single comment"
    assert comments[0].location == "Single location"


def test_create_comment_persists_in_database(db_session):
    """Test that created comments are actually persisted in the database."""
    comment_data = CommentCreate(
        text="Persistent comment",
        location="Persistent location",
        image_url="https://example.com/persistent.jpg"
    )

    created_comment = crud.create_comment(db_session, comment_data)
    comment_id = created_comment.id

    # Query the database directly to verify persistence
    db_comment = db_session.query(Comment).filter(Comment.id == comment_id).first()

    assert db_comment is not None
    assert db_comment.text == "Persistent comment"
    assert db_comment.location == "Persistent location"
    assert db_comment.image_url == "https://example.com/persistent.jpg"

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


def test_get_comments_multiple_ordered_by_date(db_session):
    """Test creating and getting multiple comments."""
    from datetime import datetime, timedelta

    # Create first comment with an earlier timestamp
    comment1_data = CommentCreate(
        text="First comment",
        location="Location 1",
        image_url=None
    )
    crud.create_comment(db_session, comment1_data)

    # Create second comment with a later timestamp
    comment2_data = CommentCreate(
        text="Second comment",
        location="Location 2",
        image_url=None
    )
    crud.create_comment(db_session, comment2_data)

    comments = crud.get_comments(db_session)

    assert len(comments) == 2
    # Most recent comment should be first (ordered by created_at desc)
    assert comments[0].text == "Second comment"
    assert comments[1].text == "First comment"
    # Verify the ordering by comparing timestamps
    assert comments[0].created_at > comments[1].created_at


def test_create_comment_with_special_characters(db_session):
    """Test creating a comment with special characters."""
    comment_data = CommentCreate(
        text="Comment with special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./ àáâãäåæçèéêë",
        location="Location with émojis 🎉🎊",
        image_url=None
    )

    created_comment = crud.create_comment(db_session, comment_data)

    assert created_comment.text == "Comment with special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./ àáâãäåæçèéêë"
    assert created_comment.location == "Location with émojis 🎉🎊"


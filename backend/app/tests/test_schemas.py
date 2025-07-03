"""
Unit tests for Pydantic schemas.

These tests verify that the schemas properly validate input data
and handle edge cases correctly.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from ..schemas import CommentCreate, Comment


class TestCommentCreate:
    """Test the CommentCreate schema."""

    def test_valid_comment_create_with_image(self):
        """Test creating a valid CommentCreate with image URL."""
        comment_data = {
            "text": "Test comment",
            "location": "Test location",
            "image_url": "https://example.com/image.jpg"
        }

        comment = CommentCreate(**comment_data)

        assert comment.text == "Test comment"
        assert comment.location == "Test location"
        assert comment.image_url == "https://example.com/image.jpg"

    def test_valid_comment_create_without_image(self):
        """Test creating a valid CommentCreate without image URL."""
        comment_data = {
            "text": "Test comment",
            "location": "Test location",
            "image_url": None
        }

        comment = CommentCreate(**comment_data)

        assert comment.text == "Test comment"
        assert comment.location == "Test location"
        assert comment.image_url is None

    def test_comment_create_missing_image_url_field(self):
        """Test that image_url field is required and raises ValidationError when missing."""
        comment_data = {
            "text": "Test comment",
            "location": "Test location"
        }

        with pytest.raises(ValidationError) as exc_info:
            CommentCreate(**comment_data)

        assert "image_url" in str(exc_info.value)

    def test_comment_create_missing_required_text(self):
        """Test that missing text field raises ValidationError."""
        comment_data = {
            "location": "Test location",
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            CommentCreate(**comment_data)

        assert "text" in str(exc_info.value)

    def test_comment_create_missing_required_location(self):
        """Test that missing location field raises ValidationError."""
        comment_data = {
            "text": "Test comment",
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            CommentCreate(**comment_data)

        assert "location" in str(exc_info.value)

    def test_comment_create_empty_text(self):
        """Test creating a comment with empty text."""
        comment_data = {
            "text": "",
            "location": "Test location",
            "image_url": None
        }

        comment = CommentCreate(**comment_data)
        assert comment.text == ""

    def test_comment_create_empty_location(self):
        """Test creating a comment with empty location."""
        comment_data = {
            "text": "Test comment",
            "location": "",
            "image_url": None
        }

        comment = CommentCreate(**comment_data)
        assert comment.location == ""

    def test_comment_create_with_special_characters(self):
        """Test creating a comment with special characters."""
        comment_data = {
            "text": "Comment with special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./ àáâãäåæçèéêë",
            "location": "Location with émojis 🎉🎊",
            "image_url": "https://example.com/image-with-special_chars.jpg"
        }

        comment = CommentCreate(**comment_data)

        assert comment.text == "Comment with special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./ àáâãäåæçèéêë"
        assert comment.location == "Location with émojis 🎉🎊"
        assert comment.image_url == "https://example.com/image-with-special_chars.jpg"


class TestComment:
    """Test the Comment schema."""

    def test_valid_comment_with_image(self):
        """Test creating a valid Comment with image URL."""
        comment_data = {
            "id": 1,
            "text": "Test comment",
            "location": "Test location",
            "created_at": datetime.now(),
            "image_url": "https://example.com/image.jpg"
        }

        comment = Comment(**comment_data)

        assert comment.id == 1
        assert comment.text == "Test comment"
        assert comment.location == "Test location"
        assert isinstance(comment.created_at, datetime)
        assert comment.image_url == "https://example.com/image.jpg"

    def test_valid_comment_without_image(self):
        """Test creating a valid Comment without image URL."""
        comment_data = {
            "id": 2,
            "text": "Test comment",
            "location": "Test location",
            "created_at": datetime.now(),
            "image_url": None
        }

        comment = Comment(**comment_data)

        assert comment.id == 2
        assert comment.text == "Test comment"
        assert comment.location == "Test location"
        assert isinstance(comment.created_at, datetime)
        assert comment.image_url is None

    def test_comment_missing_required_id(self):
        """Test that missing id field raises ValidationError."""
        comment_data = {
            "text": "Test comment",
            "location": "Test location",
            "created_at": datetime.now(),
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            Comment(**comment_data)

        assert "id" in str(exc_info.value)

    def test_comment_missing_required_created_at(self):
        """Test that missing created_at field raises ValidationError."""
        comment_data = {
            "id": 1,
            "text": "Test comment",
            "location": "Test location",
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            Comment(**comment_data)

        assert "created_at" in str(exc_info.value)

    def test_comment_invalid_id_type(self):
        """Test that invalid id type raises ValidationError."""
        comment_data = {
            "id": "not_an_integer",
            "text": "Test comment",
            "location": "Test location",
            "created_at": datetime.now(),
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            Comment(**comment_data)

        assert "id" in str(exc_info.value)

    def test_comment_invalid_created_at_type(self):
        """Test that invalid created_at type raises ValidationError."""
        comment_data = {
            "id": 1,
            "text": "Test comment",
            "location": "Test location",
            "created_at": "not_a_datetime",
            "image_url": None
        }

        with pytest.raises(ValidationError) as exc_info:
            Comment(**comment_data)

        assert "created_at" in str(exc_info.value)

    def test_comment_from_attributes_config(self):
        """Test that the Config.from_attributes is properly set."""
        assert Comment.model_config.get("from_attributes") is True
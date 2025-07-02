import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import patch
from main import app  # Adjust import based on your actual entry point
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# Test DB setup/teardown (in-memory or test DB)
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.mark.asyncio
async def test_get_comments_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/comments")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_comment_without_image():
    data = {"text": "Saw Tilit!", "location": "Brooklyn"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/comments", data=data)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["text"] == "Saw Tilit!"
    assert body["location"] == "Brooklyn"
    assert body["image_url"] is None


@pytest.mark.asyncio
async def test_create_comment_with_image(tmp_path):
    # Create a dummy image file
    img_path = tmp_path / "test.jpg"
    img_path.write_bytes(b"fake-image-bytes")

    with open(img_path, "rb") as img_file:
        files = {"file": ("test.jpg", img_file, "image/jpeg")}
        data = {"text": "Saw Tilit near the park", "location": "Park Slope"}

        with patch("app.utils.s3_tools.upload_image", return_value="https://s3.com/fake-image.jpg"):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post("/comments", data=data, files=files)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["text"] == "Saw Tilit near the park"
    assert body["location"] == "Park Slope"
    assert body["image_url"] == "https://s3.com/fake-image.jpg"


@pytest.mark.asyncio
async def test_get_comments_after_creation():
    # Create a comment first
    data = {"text": "Saw Tilit again!", "location": "Williamsburg"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/comments", data=data)
        response = await ac.get("/comments")

    assert response.status_code == status.HTTP_200_OK
    comments = response.json()
    assert len(comments) == 1
    assert comments[0]["text"] == "Saw Tilit again!"

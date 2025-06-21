import os
import shutil
import pytest
from fastapi.testclient import TestClient
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app, UPLOAD_DIR

client = TestClient(app)


# Cleanup uploads folder before and after tests
@pytest.fixture(scope="function", autouse=True)
def cleanup_uploads():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)
    yield
    shutil.rmtree(UPLOAD_DIR)


def test_upload_and_get_submission():
    # Prepare dummy image file
    file_content = b"dummy image content"
    file_path = "test.jpg"
    with open(file_path, "wb") as f:
        f.write(file_content)

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"image": ("test.jpg", f, "image/jpeg")},
            data={"location": "Central Park", "comment": "Seen near the fountain"}
        )

    os.remove(file_path)

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Now test retrieval
    res = client.get("/submissions")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["location"] == "Central Park"
    assert "uploads/" in data[0]["image_url"]

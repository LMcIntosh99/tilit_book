def test_create_and_get_comments(client):
    response = client.post(
        "/comments",
        data={
            "text": "Test Text",
            "location": "Test Location"
        }
    )
    assert response.status_code == 200
    comment = response.json()
    assert comment["text"] == "Test Text"
    assert comment["location"] == "Test Location"
    assert comment["image_url"] is None  # no image uploaded

    response = client.get("/comments")
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert any(c["text"] == "Test Text" and c["location"] == "Test Location" for c in comments)

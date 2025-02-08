import pytest
from app import app
from unittest.mock import patch
from io import BytesIO

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_resume(client):
    sample_resume = BytesIO(b"John Doe\njohn.doe@example.com\n+1234567890")
    data = {"file": (sample_resume, "resume.pdf")}

    response = client.post("/api/upload-resume", data=data, content_type="multipart/form-data")
    assert response.status_code == 202
    assert "File uploaded, processing in background" in response.get_json()["message"]

@patch("app.controllers.resume_controller.process_resume_async.apply_async")
def test_async_processing(mock_task, client):
    sample_resume = BytesIO(b"John Doe\nSoftware Engineer")
    data = {"file": (sample_resume, "resume.pdf")}

    response = client.post("/api/upload-resume", data=data, content_type="multipart/form-data")
    assert response.status_code == 202
    mock_task.assert_called_once()

def test_get_resumes(client):
    response = client.get("/api/resumes?page=1&limit=5")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

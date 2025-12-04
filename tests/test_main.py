from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Notes API"}

def test_create_note():
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert "id" in data

def test_read_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_note():
    # Create a note first
    create_response = client.post(
        "/notes/",
        json={"title": "Note to Read", "content": "Content"}
    )
    note_id = create_response.json()["id"]
    
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Note to Read"

def test_update_note():
    # Create a note first
    create_response = client.post(
        "/notes/",
        json={"title": "Note to Update", "content": "Original Content"}
    )
    note_id = create_response.json()["id"]
    
    response = client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Title", "content": "Updated Content"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_note():
    # Create a note first
    create_response = client.post(
        "/notes/",
        json={"title": "Note to Delete", "content": "Content"}
    )
    note_id = create_response.json()["id"]
    
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404

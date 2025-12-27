import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # Try to sign up again
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First sign up
    client.post("/activities/Chess%20Club/signup?email=remove@mergington.edu")
    
    # Then unregister
    response = client.delete("/activities/Chess%20Club/signup?email=remove@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "remove@mergington.edu" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
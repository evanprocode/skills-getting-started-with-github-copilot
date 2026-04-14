"""Pytest configuration and shared fixtures for API tests."""

import pytest
import copy
from fastapi.testclient import TestClient
import src.app


# Store the original activities for reference
ORIGINAL_ACTIVITIES = None


@pytest.fixture
def sample_activities():
    """Return a fresh copy of sample activities for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture(autouse=True)
def reset_app_state(monkeypatch, sample_activities):
    """Reset app.activities to test data before each test using monkeypatch."""
    # Create a fresh copy of test data for this test
    test_activities = copy.deepcopy(sample_activities)
    # Monkeypatch the module-level activities variable
    monkeypatch.setattr(src.app, "activities", test_activities)
    yield


@pytest.fixture
def client():
    """Return TestClient for making requests to the app."""
    return TestClient(src.app.app)

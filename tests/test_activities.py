"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client, sample_activities):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == len(sample_activities)
        assert set(data.keys()) == set(sample_activities.keys())

    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        response = client.get("/activities")
        data = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in data.items():
            assert set(activity_data.keys()) == required_fields, \
                f"Activity '{activity_name}' missing required fields"

    def test_participants_is_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"

    def test_max_participants_is_integer(self, client):
        """Test that max_participants is an integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants should be integer"

    def test_activities_contain_sample_data(self, client):
        """Test that response contains expected sample activity."""
        response = client.get("/activities")
        data = response.json()
        
        assert "Chess Club" in data
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert len(data["Chess Club"]["participants"]) == 2

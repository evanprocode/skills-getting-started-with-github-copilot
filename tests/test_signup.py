"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for activity signup endpoint."""

    def test_signup_returns_200_on_success(self, client):
        """Test that signup returns 200 status on successful signup."""
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_adds_participant_to_list(self, client):
        """Test that signup actually adds the participant to the activity."""
        email = "newstudent@mergington.edu"
        activity = "Gym Class"
        
        # Verify student not already signed up
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
        
        # Sign up
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Verify student is now signed up
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

    def test_signup_returns_success_message(self, client):
        """Test that signup returns a success message."""
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_duplicate_returns_400(self, client):
        """Test that signing up twice for same activity returns 400."""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signup for nonexistent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_multiple_different_activities(self, client):
        """Test that same student can sign up for multiple different activities."""
        email = "alice@mergington.edu"
        
        # Sign up for first activity
        response1 = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for second activity
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups worked
        response = client.get("/activities")
        data = response.json()
        assert email in data["Gym Class"]["participants"]
        assert email in data["Chess Club"]["participants"]

    def test_signup_with_special_characters_in_email(self, client):
        """Test that signup works with special characters in email (URL encoded)."""
        email = "test+special@mergington.edu"
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify it was added
        response = client.get("/activities")
        assert email in response.json()["Gym Class"]["participants"]

    def test_signup_increments_participant_count(self, client):
        """Test that signup increases the participant count."""
        activity = "Gym Class"
        
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        client.post(f"/activities/{activity}/signup", params={"email": "new@mergington.edu"})
        
        response = client.get("/activities")
        new_count = len(response.json()[activity]["participants"])
        
        assert new_count == initial_count + 1

"""Tests for DELETE /activities/{activity_name}/signup endpoint."""

import pytest


class TestUnregister:
    """Test suite for activity unregister endpoint."""

    def test_unregister_returns_200_on_success(self, client):
        """Test that unregister returns 200 status on successful unregister."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_unregister_removes_participant_from_list(self, client):
        """Test that unregister actually removes the participant."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify student is signed up
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        client.delete(f"/activities/{activity}/signup", params={"email": email})
        
        # Verify student is no longer signed up
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_unregister_returns_success_message(self, client):
        """Test that unregister returns a success message."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert "michael@mergington.edu" in data["message"]

    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregister from nonexistent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_signed_up_returns_404(self, client):
        """Test that unregistering a student not signed up returns 404."""
        response = client.delete(
            "/activities/Gym Class/signup",
            params={"email": "notasignedupstudent@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Student not signed up"

    def test_unregister_twice_returns_404_second_time(self, client):
        """Test that unregistering twice for same activity returns 404 on second attempt."""
        email = "daniel@mergington.edu"
        activity = "Chess Club"
        
        # First unregister should succeed
        response1 = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response2.status_code == 404
        assert response2.json()["detail"] == "Student not signed up"

    def test_unregister_decrements_participant_count(self, client):
        """Test that unregister decreases the participant count."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        client.delete(f"/activities/{activity}/signup", params={"email": email})
        
        response = client.get("/activities")
        new_count = len(response.json()[activity]["participants"])
        
        assert new_count == initial_count - 1

    def test_signup_then_unregister_then_signup_again(self, client):
        """Test signup, unregister, then signup again for same activity."""
        email = "alice@mergington.edu"
        activity = "Gym Class"
        
        # First signup
        response1 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response1.status_code == 200
        
        # Unregister
        response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response2.status_code == 200
        
        # Second signup (should succeed since we unregistered)
        response3 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response3.status_code == 200
        
        # Verify final state
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

    def test_unregister_with_special_characters_in_email(self, client):
        """Test that unregister works with special characters in email."""
        email = "test+special@mergington.edu"
        activity = "Gym Class"
        
        # First sign up
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Then unregister
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200
        
        # Verify removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

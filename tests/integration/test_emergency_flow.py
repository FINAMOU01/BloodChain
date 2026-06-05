import pytest
from rest_framework.test import APIClient
from django.test import TestCase


class EmergencyFlowTest(TestCase):
    """Integration tests for the emergency notification flow."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()

    def test_emergency_alert_created(self):
        """Test emergency alert creation returns 201 with is_emergency True."""
        url = "/api/notifications/alert/"
        payload = {
            "recipient_email": "donor@test.com",
            "message": "Urgent blood needed",
            "blood_type_needed": "O+",
            "hospital_name": "Central Hospital",
            "is_emergency": True
        }
        response = self.client.post(url, payload, format="json")
        assert response.status_code == 201
        assert response.data["is_emergency"] is True

    def test_notification_list(self):
        """Test retrieving notification list returns 200."""
        url = "/api/notifications/list/"
        response = self.client.get(url)
        assert response.status_code == 200

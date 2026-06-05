from django.test import TestCase
from rest_framework.test import APIClient
from app.models import Notification
from unittest.mock import patch


class NotificationsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("app.tasks.send_push_notification")
    @patch("app.tasks.send_emergency_alert")
    def test_create_emergency_alert(self, mock_send_emergency_alert, mock_send_push_notification):
        payload = {
            "recipient_email": "donor@test.com",
            "message": "Urgent",
            "blood_type_needed": "O+",
            "hospital_name": "Central Hospital",
            "is_emergency": True,
        }
        response = self.client.post("/api/notifications/alert/", payload, format="json")
        assert response.status_code == 201
        assert Notification.objects.count() == 1

    def test_list_notifications(self):
        Notification.objects.create(
            recipient_email="test@user.com",
            message="Test Message",
            blood_type_needed="A+",
            hospital_name="H",
        )
        response = self.client.get("/api/notifications/list/")
        assert response.status_code == 200

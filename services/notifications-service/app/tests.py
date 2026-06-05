from django.test import TestCase
from rest_framework.test import APIClient
from .models import Notification


class NotificationModelTest(TestCase):
    def test_create_notification(self):
        n = Notification.objects.create(
            recipient_email="test@test.com",
            message="Urgent need",
            blood_type_needed="A+",
            hospital_name="City Hospital",
            is_emergency=True,
        )
        assert n.recipient_email == "test@test.com"
        assert n.is_sent is False
        assert n.is_emergency is True

    def test_notification_str(self):
        n = Notification.objects.create(
            recipient_email="donor@test.com",
            message="Test",
            blood_type_needed="O-",
            hospital_name="General",
        )
        assert str(n) == "donor@test.com - O-"

    def test_default_is_sent_false(self):
        n = Notification.objects.create(
            recipient_email="a@b.com", message="Hi", blood_type_needed="B+", hospital_name="H"
        )
        assert n.is_sent is False

    def test_default_is_emergency_false(self):
        n = Notification.objects.create(
            recipient_email="a@b.com", message="Hi", blood_type_needed="B+", hospital_name="H"
        )
        assert n.is_emergency is False


class EmergencyAlertAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_emergency_alert_success(self):
        payload = {
            "recipient_email": "donor@test.com",
            "message": "Urgent blood needed",
            "blood_type_needed": "A+",
            "hospital_name": "Central Hospital",
            "is_emergency": True,
        }
        response = self.client.post("/api/notifications/alert/", payload, format="json")
        assert response.status_code == 201
        assert response.data["recipient_email"] == "donor@test.com"
        assert response.data["is_emergency"] is True
        assert Notification.objects.count() == 1

    def test_create_alert_missing_required_field(self):
        payload = {
            "recipient_email": "donor@test.com",
            "message": "Urgent",
        }
        response = self.client.post("/api/notifications/alert/", payload, format="json")
        assert response.status_code == 400

    def test_create_alert_invalid_blood_type(self):
        payload = {
            "recipient_email": "d@t.com",
            "message": "Need blood",
            "blood_type_needed": "INVALID",
            "hospital_name": "H",
        }
        response = self.client.post("/api/notifications/alert/", payload, format="json")
        assert response.status_code == 400

    def test_list_notifications_empty(self):
        response = self.client.get("/api/notifications/list/")
        assert response.status_code == 200
        assert response.data == []

    def test_list_notifications_with_data(self):
        Notification.objects.create(
            recipient_email="a@b.com", message="M1", blood_type_needed="O+", hospital_name="H"
        )
        Notification.objects.create(
            recipient_email="b@c.com", message="M2", blood_type_needed="A-", hospital_name="H2"
        )
        response = self.client.get("/api/notifications/list/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_create_alert_sets_is_sent_false(self):
        payload = {
            "recipient_email": "d@d.com",
            "message": "Test",
            "blood_type_needed": "AB+",
            "hospital_name": "H",
        }
        response = self.client.post("/api/notifications/alert/", payload, format="json")
        assert response.status_code == 201
        assert response.data["is_sent"] is False

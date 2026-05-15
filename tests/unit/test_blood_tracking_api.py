from django.test import TestCase
from rest_framework.test import APIClient
from blood_tracking.models import BloodBag


class BloodTrackingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_collect_blood_bag(self):
        payload = {
            "blood_type": "A+"
        }
        response = self.client.post("/api/tracking/bag/collect/", payload, format="json")
        assert response.status_code == 201
        assert "bag_id" in response.data

    def test_collect_invalid_blood_type(self):
        payload = {
            "blood_type": "ZZ+"
        }
        response = self.client.post("/api/tracking/bag/collect/", payload, format="json")
        assert response.status_code == 400

    def test_get_blood_bag_detail(self):
        bag = BloodBag.objects.create(blood_type="O-")
        response = self.client.get(f"/api/tracking/bag/{bag.bag_id}/")
        assert response.status_code == 200
        assert "blood_type" in response.data

    def test_get_nonexistent_bag(self):
        response = self.client.get("/api/tracking/bag/00000000-0000-0000-0000-000000000000/")
        assert response.status_code == 404

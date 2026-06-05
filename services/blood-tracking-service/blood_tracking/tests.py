from django.test import TestCase
from rest_framework.test import APIClient
from .models import BloodBag


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

    def test_list_bags_by_donor_email(self):
        bag1 = BloodBag.objects.create(blood_type="O+", donor_email="donor@test.com", volume_ml=450)
        bag2 = BloodBag.objects.create(blood_type="O+", donor_email="donor@test.com", volume_ml=500)
        BloodBag.objects.create(blood_type="A+", donor_email="other@test.com")  # should be excluded
        response = self.client.get(f"/api/tracking/bags/donor/donor@test.com/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["bag_id"] == str(bag2.bag_id)  # ordered by -collected_at, bag2 created second/newer

    def test_list_bags_by_donor_email_no_results(self):
        response = self.client.get("/api/tracking/bags/donor/nobody@test.com/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

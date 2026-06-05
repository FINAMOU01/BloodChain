from django.test import TestCase
from rest_framework.test import APIClient
from donor.models import Donor


class DonorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_donor_success(self):
        payload = {
            "full_name": "Test User",
            "email": "test@user.com",
            "phone_number": "+1234567890",
            "blood_type": "A+",
            "date_of_birth": "1990-01-01"
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 201
        assert Donor.objects.count() == 1

    def test_register_donor_missing_field(self):
        payload = {
            "full_name": "Test User",
            "phone_number": "+1234567890",
            "blood_type": "A+",
            "date_of_birth": "1990-01-01"
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_underage_donor(self):
        payload = {
            "full_name": "Underage User",
            "email": "child@user.com",
            "phone_number": "+1234567890",
            "blood_type": "A+",
            "date_of_birth": "2015-01-01"
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 400

    def test_get_donor_profile(self):
        donor = Donor.objects.create(
            full_name="Profile User",
            email="profile@user.com",
            phone_number="+0987654321",
            blood_type="O+",
            date_of_birth="1985-05-05"
        )
        response = self.client.get(f"/api/donor/profile/{donor.email}/")
        assert response.status_code == 200
        assert "full_name" in response.data

    def test_get_nonexistent_profile(self):
        response = self.client.get("/api/donor/profile/nobody@test.com/")
        assert response.status_code == 404

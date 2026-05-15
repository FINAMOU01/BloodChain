from django.test import TestCase
from rest_framework.test import APIClient
from hospital.models import Hospital, BloodRequest


class HospitalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hospital = Hospital.objects.create(
            name="Central Hospital",
            location="Yaounde",
            contact_email="central@hospital.com",
            contact_phone="+237600000002"
        )

    def test_create_blood_request(self):
        payload = {
            "hospital": self.hospital.id,
            "blood_type": "O+",
            "units_needed": 5
        }
        response = self.client.post("/api/hospital/request/", payload, format="json")
        assert response.status_code == 201

    def test_list_blood_requests(self):
        BloodRequest.objects.create(
            hospital=self.hospital,
            blood_type="O+",
            units_needed=2
        )
        response = self.client.get("/api/hospital/requests/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_blood_stock(self):
        response = self.client.get(f"/api/hospital/stock/{self.hospital.id}/")
        assert response.status_code == 200
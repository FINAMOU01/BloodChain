from django.test import TestCase
from rest_framework.test import APIClient
from .models import Hospital, BloodStock, BloodRequest


class HospitalModelTest(TestCase):
    def test_create_hospital(self):
        h = Hospital.objects.create(
            name="City Hospital",
            location="Downtown",
            contact_email="admin@city.com",
            contact_phone="+1234567890",
        )
        assert h.name == "City Hospital"
        assert h.is_active is True
        assert str(h) == "City Hospital"

    def test_hospital_default_active(self):
        h = Hospital.objects.create(name="H", location="L", contact_email="e@e.com", contact_phone="+1")
        assert h.is_active is True


class BloodStockModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="H", location="L", contact_email="e@e.com", contact_phone="+1"
        )

    def test_create_blood_stock(self):
        bs = BloodStock.objects.create(hospital=self.hospital, blood_type="A+", units_available=10)
        assert bs.blood_type == "A+"
        assert bs.units_available == 10
        assert str(bs) == "H - A+"

    def test_stock_default_units(self):
        bs = BloodStock.objects.create(hospital=self.hospital, blood_type="O-")
        assert bs.units_available == 0


class BloodRequestModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="H", location="L", contact_email="e@e.com", contact_phone="+1"
        )

    def test_create_blood_request(self):
        br = BloodRequest.objects.create(
            hospital=self.hospital, blood_type="B+", units_needed=5
        )
        assert br.status == "pending"
        assert str(br) == "H - B+ - pending"

    def test_request_default_status_pending(self):
        br = BloodRequest.objects.create(
            hospital=self.hospital, blood_type="A-", units_needed=3
        )
        assert br.status == "pending"


class HospitalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_hospital_success(self):
        payload = {
            "name": "Central Hospital",
            "location": "Main Street",
            "contact_email": "admin@central.com",
            "contact_phone": "+1234567890",
        }
        response = self.client.post("/api/hospital/register/", payload, format="json")
        assert response.status_code == 201
        assert Hospital.objects.count() == 1

    def test_register_hospital_missing_field(self):
        payload = {"name": "Incomplete"}
        response = self.client.post("/api/hospital/register/", payload, format="json")
        assert response.status_code == 400

    def test_get_hospital_profile(self):
        Hospital.objects.create(
            name="General", location="Uptown", contact_email="gen@g.com", contact_phone="+1"
        )
        response = self.client.get("/api/hospital/profile/gen@g.com/")
        assert response.status_code == 200
        assert response.data["name"] == "General"

    def test_get_nonexistent_profile_returns_empty(self):
        response = self.client.get("/api/hospital/profile/unknown@test.com/")
        assert response.status_code == 200
        assert response.data["name"] == ""

    def test_update_hospital_profile(self):
        Hospital.objects.create(
            name="Old", location="Here", contact_email="up@test.com", contact_phone="+1"
        )
        response = self.client.patch(
            "/api/hospital/profile/up@test.com/update/",
            {"name": "New Name"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == "New Name"

    def test_update_nonexistent_hospital_creates(self):
        response = self.client.patch(
            "/api/hospital/profile/new@test.com/update/",
            {"name": "New Hosp", "location": "Here", "contact_phone": "+1"},
            format="json",
        )
        assert response.status_code == 200
        assert Hospital.objects.count() == 1

    def test_create_blood_request(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        payload = {"hospital": hosp.pk, "blood_type": "O+", "units_needed": 3}
        response = self.client.post("/api/hospital/request/", payload, format="json")
        assert response.status_code == 201
        assert BloodRequest.objects.count() == 1

    def test_list_blood_requests(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        BloodRequest.objects.create(hospital=hosp, blood_type="A+", units_needed=2)
        BloodRequest.objects.create(hospital=hosp, blood_type="B-", units_needed=4)
        response = self.client.get("/api/hospital/requests/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_get_blood_request_detail(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        br = BloodRequest.objects.create(hospital=hosp, blood_type="AB+", units_needed=1)
        response = self.client.get(f"/api/hospital/requests/{br.pk}/")
        assert response.status_code == 200
        assert response.data["blood_type"] == "AB+"

    def test_get_nonexistent_blood_request(self):
        response = self.client.get("/api/hospital/requests/9999/")
        assert response.status_code == 404

    def test_update_blood_request(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        br = BloodRequest.objects.create(hospital=hosp, blood_type="O-", units_needed=5)
        response = self.client.patch(
            f"/api/hospital/requests/{br.pk}/update/",
            {"status": "fulfilled"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["status"] == "fulfilled"

    def test_update_nonexistent_blood_request(self):
        response = self.client.patch("/api/hospital/requests/9999/update/", {"status": "fulfilled"}, format="json")
        assert response.status_code == 404

    def test_view_blood_stock(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        BloodStock.objects.create(hospital=hosp, blood_type="A+", units_available=10)
        BloodStock.objects.create(hospital=hosp, blood_type="O+", units_available=5)
        response = self.client.get(f"/api/hospital/stock/{hosp.pk}/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_view_blood_stock_empty(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        response = self.client.get(f"/api/hospital/stock/{hosp.pk}/")
        assert response.status_code == 200
        assert response.data == []

    def test_update_blood_stock_create_new(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        response = self.client.post(
            f"/api/hospital/stock/{hosp.pk}/update/",
            {"blood_type": "A+", "units_available": 15},
            format="json",
        )
        assert response.status_code == 200
        assert BloodStock.objects.count() == 1
        assert response.data["units_available"] == 15

    def test_update_blood_stock_existing(self):
        hosp = Hospital.objects.create(
            name="H", location="L", contact_email="h@h.com", contact_phone="+1"
        )
        BloodStock.objects.create(hospital=hosp, blood_type="B+", units_available=5)
        response = self.client.post(
            f"/api/hospital/stock/{hosp.pk}/update/",
            {"blood_type": "B+", "units_available": 20},
            format="json",
        )
        assert response.status_code == 200
        assert BloodStock.objects.count() == 1
        assert response.data["units_available"] == 20

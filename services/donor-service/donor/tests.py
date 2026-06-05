from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Donor, Appointment


class DonorModelTest(TestCase):
    def test_create_donor(self):
        d = Donor.objects.create(
            full_name="John Doe",
            email="john@test.com",
            phone_number="+1234567890",
            blood_type="O+",
            date_of_birth="1990-01-01",
        )
        assert d.full_name == "John Doe"
        assert d.is_eligible is True
        assert str(d) == "John Doe (O+)"

    def test_donor_default_eligible(self):
        d = Donor.objects.create(
            full_name="Jane", email="j@t.com", phone_number="+1", blood_type="A+", date_of_birth="1990-01-01"
        )
        assert d.is_eligible is True


class DonorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_donor_success(self):
        payload = {
            "full_name": "Test User",
            "email": "test@user.com",
            "phone_number": "+1234567890",
            "blood_type": "A+",
            "date_of_birth": "1990-01-01",
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 201
        assert Donor.objects.count() == 1

    def test_register_donor_missing_field(self):
        payload = {
            "full_name": "Test User",
            "phone_number": "+1234567890",
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_underage_donor(self):
        payload = {
            "full_name": "Child User",
            "email": "child@user.com",
            "phone_number": "+1234567890",
            "blood_type": "A+",
            "date_of_birth": "2015-01-01",
        }
        response = self.client.post("/api/donor/register/", payload, format="json")
        assert response.status_code == 400

    def test_get_donor_profile(self):
        Donor.objects.create(
            full_name="Profile User", email="profile@test.com",
            phone_number="+1", blood_type="O+", date_of_birth="1985-05-05",
        )
        response = self.client.get("/api/donor/profile/profile@test.com/")
        assert response.status_code == 200
        assert response.data["full_name"] == "Profile User"

    def test_get_nonexistent_profile(self):
        response = self.client.get("/api/donor/profile/nobody@test.com/")
        assert response.status_code == 404

    def test_list_donors(self):
        Donor.objects.create(
            full_name="A", email="a@t.com", phone_number="+1", blood_type="A+", date_of_birth="1990-01-01",
        )
        Donor.objects.create(
            full_name="B", email="b@t.com", phone_number="+2", blood_type="O-", date_of_birth="1990-01-01",
        )
        response = self.client.get("/api/donor/list/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_list_donors_filter_by_blood_type(self):
        Donor.objects.create(
            full_name="A", email="a@t.com", phone_number="+1", blood_type="A+", date_of_birth="1990-01-01",
        )
        Donor.objects.create(
            full_name="B", email="b@t.com", phone_number="+2", blood_type="O-", date_of_birth="1990-01-01",
        )
        response = self.client.get("/api/donor/list/", {"blood_type": "A+"})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["email"] == "a@t.com"

    def test_update_donor_profile(self):
        Donor.objects.create(
            full_name="Old Name", email="update@test.com",
            phone_number="+1", blood_type="B+", date_of_birth="1990-01-01",
        )
        response = self.client.patch(
            "/api/donor/profile/update@test.com/update/",
            {"full_name": "New Name"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["full_name"] == "New Name"

    def test_update_nonexistent_donor(self):
        response = self.client.patch(
            "/api/donor/profile/nobody@test.com/update/",
            {"full_name": "No One"},
            format="json",
        )
        assert response.status_code == 404

    def test_donor_eligibility_new_donor(self):
        Donor.objects.create(
            full_name="New Donor", email="new@test.com",
            phone_number="+1", blood_type="A+", date_of_birth="1990-01-01",
        )
        response = self.client.get("/api/donor/eligibility/new@test.com/")
        assert response.status_code == 200
        assert response.data["is_eligible"] is True
        assert response.data["days_until_next"] == 0

    def test_donor_eligibility_recent_donation(self):
        Donor.objects.create(
            full_name="Recent", email="recent@test.com",
            phone_number="+1", blood_type="O+", date_of_birth="1990-01-01",
        )
        Appointment.objects.create(
            donor_email="recent@test.com",
            hospital_name="H",
            appointment_type="regular",
            appointment_date=date.today() - timedelta(days=7),
            appointment_time="10:00:00",
            status="completed",
        )
        response = self.client.get("/api/donor/eligibility/recent@test.com/")
        assert response.status_code == 200
        assert response.data["is_eligible"] is False
        assert response.data["days_until_next"] > 0

    def test_eligibility_nonexistent_donor(self):
        response = self.client.get("/api/donor/eligibility/unknown@test.com/")
        assert response.status_code == 404


class AppointmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.donor = Donor.objects.create(
            full_name="Donor", email="donor@test.com",
            phone_number="+1", blood_type="A+", date_of_birth="1990-01-01",
        )

    def test_create_appointment(self):
        payload = {
            "donor_email": "donor@test.com",
            "hospital_name": "City Hospital",
            "appointment_date": (date.today() + timedelta(days=1)).isoformat(),
            "appointment_time": "10:00:00",
        }
        response = self.client.post("/api/donor/appointments/create/", payload, format="json")
        assert response.status_code == 201
        assert Appointment.objects.count() == 1

    def test_create_appointment_nonexistent_donor(self):
        payload = {
            "donor_email": "unknown@test.com",
            "hospital_name": "H",
            "appointment_date": (date.today() + timedelta(days=1)).isoformat(),
            "appointment_time": "10:00:00",
        }
        response = self.client.post("/api/donor/appointments/create/", payload, format="json")
        assert response.status_code == 400

    def test_create_appointment_past_date(self):
        payload = {
            "donor_email": "donor@test.com",
            "hospital_name": "H",
            "appointment_date": (date.today() - timedelta(days=1)).isoformat(),
            "appointment_time": "10:00:00",
        }
        response = self.client.post("/api/donor/appointments/create/", payload, format="json")
        assert response.status_code == 400

    def test_list_appointments(self):
        Appointment.objects.create(
            donor_email="donor@test.com",
            hospital_name="H", appointment_date=date.today(), appointment_time="10:00:00",
        )
        Appointment.objects.create(
            donor_email="donor@test.com",
            hospital_name="H2", appointment_date=date.today(), appointment_time="11:00:00",
        )
        response = self.client.get("/api/donor/appointments/donor@test.com/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_update_appointment_status(self):
        appt = Appointment.objects.create(
            donor_email="donor@test.com",
            hospital_name="H", appointment_date=date.today(), appointment_time="10:00:00",
        )
        response = self.client.patch(
            f"/api/donor/appointments/{appt.pk}/update/",
            {"status": "cancelled"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["status"] == "cancelled"

    def test_update_nonexistent_appointment(self):
        response = self.client.patch("/api/donor/appointments/9999/update/", {"status": "cancelled"}, format="json")
        assert response.status_code == 404

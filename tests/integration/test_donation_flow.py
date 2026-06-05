import requests
import pytest

BASE = "http://localhost"


class TestDonationFlow:
    """End-to-end integration tests for the donation flow.

    Requires all Docker services to be running (docker-compose up -d).
    Runs against the nginx reverse proxy at localhost:80.
    """

    def setup_method(self):
        self.donor_email = f"donor_{id(self)}@test.com"

    def _register_donor(self, email=None):
        payload = {
            "full_name": "John Doe",
            "email": email or self.donor_email,
            "phone_number": "+237600000001",
            "blood_type": "O+",
            "date_of_birth": "1990-03-15",
        }
        return requests.post(f"{BASE}/api/donor/register/", json=payload)

    def test_01_donor_registration(self):
        resp = self._register_donor()
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["email"] == self.donor_email
        assert data["blood_type"] == "O+"

    def test_02_duplicate_donor_rejected(self):
        self._register_donor()
        resp = self._register_donor()
        assert resp.status_code == 400

    def test_03_underage_donor_rejected(self):
        payload = {
            "full_name": "Child",
            "email": "child@test.com",
            "phone_number": "+1",
            "blood_type": "A+",
            "date_of_birth": "2015-01-01",
        }
        resp = requests.post(f"{BASE}/api/donor/register/", json=payload)
        assert resp.status_code == 400

    def test_04_get_donor_profile(self):
        self._register_donor()
        resp = requests.get(f"{BASE}/api/donor/profile/{self.donor_email}/")
        assert resp.status_code == 200
        assert resp.json()["email"] == self.donor_email

    def test_05_donor_list_all(self):
        self._register_donor()
        resp = requests.get(f"{BASE}/api/donor/list/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_06_create_appointment(self):
        self._register_donor()
        from datetime import date, timedelta

        payload = {
            "donor_email": self.donor_email,
            "hospital_name": "Central Hospital",
            "appointment_date": (date.today() + timedelta(days=7)).isoformat(),
            "appointment_time": "10:00:00",
        }
        resp = requests.post(f"{BASE}/api/donor/appointments/create/", json=payload)
        assert resp.status_code == 201, resp.text
        assert resp.json()["donor_email"] == self.donor_email

    def test_07_update_appointment_status(self):
        self._register_donor()
        from datetime import date, timedelta

        # Create appointment
        payload = {
            "donor_email": self.donor_email,
            "hospital_name": "H",
            "appointment_date": (date.today() + timedelta(days=7)).isoformat(),
            "appointment_time": "10:00:00",
        }
        resp = requests.post(f"{BASE}/api/donor/appointments/create/", json=payload)
        appt_id = resp.json()["id"]

        # Update to completed
        resp = requests.patch(
            f"{BASE}/api/donor/appointments/{appt_id}/update/",
            json={"status": "completed"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"

    def test_08_check_eligibility(self):
        self._register_donor()
        resp = requests.get(f"{BASE}/api/donor/eligibility/{self.donor_email}/")
        assert resp.status_code == 200
        data = resp.json()
        assert "is_eligible" in data
        assert "days_until_next" in data

    def test_09_hospital_flow(self):
        # Register hospital
        hosp_email = f"admin_{id(self)}@hospital.com"
        payload = {
            "name": "Test Hospital",
            "location": "Downtown",
            "contact_email": hosp_email,
            "contact_phone": "+1234567890",
        }
        resp = requests.post(f"{BASE}/api/hospital/register/", json=payload)
        assert resp.status_code == 201, resp.text
        hosp_id = resp.json()["id"]

        # Get profile
        resp = requests.get(f"{BASE}/api/hospital/profile/{hosp_email}/")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Test Hospital"

        # Update blood stock
        resp = requests.post(
            f"{BASE}/api/hospital/stock/{hosp_id}/update/",
            json={"blood_type": "O+", "units_available": 50},
        )
        assert resp.status_code == 200
        assert resp.json()["units_available"] == 50

        # Create blood request
        resp = requests.post(
            f"{BASE}/api/hospital/request/",
            json={"hospital": hosp_id, "blood_type": "O+", "units_needed": 10},
        )
        assert resp.status_code == 201

    def test_10_emergency_alert(self):
        resp = requests.post(
            f"{BASE}/api/notifications/alert/",
            json={
                "recipient_email": "donor@test.com",
                "message": "Urgent blood needed",
                "blood_type_needed": "O+",
                "hospital_name": "City Hospital",
                "is_emergency": True,
            },
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["is_emergency"] is True

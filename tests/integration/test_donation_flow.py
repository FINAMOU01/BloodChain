import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase


class DonationFlowTest(TestCase):
    """Integration tests for the donation flow."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()

    def test_donor_registration(self, donor_payload):
        """Test donor registration returns 201 and includes email in response."""
        url = reverse("donor-register")
        response = self.client.post(url, donor_payload, format="json")
        assert response.status_code == 201
        assert "email" in response.data

    def test_duplicate_donor_rejected(self, donor_payload):
        """Test registering duplicate donor returns 400."""
        url = reverse("donor-register")
        # First registration
        self.client.post(url, donor_payload, format="json")
        # Duplicate registration
        response = self.client.post(url, donor_payload, format="json")
        assert response.status_code == 400

    def test_underage_donor_rejected(self, donor_payload):
        """Test registering underage donor returns 400."""
        url = reverse("donor-register")
        donor_payload["date_of_birth"] = "2015-01-01"
        response = self.client.post(url, donor_payload, format="json")
        assert response.status_code == 400

    def test_blood_bag_collection(self, blood_bag_payload):
        """Test blood bag collection returns 201 and includes bag_id in response."""
        url = reverse("bag-collect")
        response = self.client.post(url, blood_bag_payload, format="json")
        assert response.status_code == 201
        assert "bag_id" in response.data

    def test_full_donation_flow(self, donor_payload, blood_bag_payload):
        """Test full donation flow: donor registration + blood bag collection."""
        # Register donor
        donor_url = reverse("donor-register")
        donor_response = self.client.post(donor_url, donor_payload, format="json")
        assert donor_response.status_code == 201

        # Collect blood bag
        bag_url = reverse("bag-collect")
        bag_response = self.client.post(bag_url, blood_bag_payload, format="json")
        assert bag_response.status_code == 201

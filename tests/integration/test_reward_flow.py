import pytest
from rest_framework.test import APIClient
from django.test import TestCase


class RewardFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_reward_minted(self):
        payload = {
            "donor_email": "donor@test.com",
            "donor_wallet": "0x000000000000000000000000000000000000dead",
            "tokens_minted": 10,
            "bag_id": "bag-001"
        }
        response = self.client.post("/api/rewards/mint/", payload, format="json")
        assert response.status_code == 201
        assert response.data["tokens_minted"] == 10

    def test_reward_list(self):
        response = self.client.get("/api/rewards/list/")
        assert response.status_code == 200

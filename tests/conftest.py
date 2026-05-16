import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Returns an API client for testing."""
    return APIClient()


@pytest.fixture
def donor_payload():
    """Returns a donor payload dictionary."""
    return {
        "full_name": "John Doe",
        "email": "john@test.com",
        "phone_number": "+237600000001",
        "blood_type": "O+",
        "date_of_birth": "1995-03-15"
    }


@pytest.fixture
def blood_request_payload():
    """Returns a blood request payload dictionary."""
    return {
        "hospital": 1,
        "blood_type": "O+",
        "units_needed": 5
    }


@pytest.fixture
def blood_bag_payload():
    """Returns a blood bag payload dictionary."""
    return {
        "blood_type": "A+"
    }


@pytest.fixture
def reward_payload():
    """Returns a reward payload dictionary."""
    return {
        "donor_email": "john@test.com",
        "donor_wallet": "0x000000000000000000000000000000000000dead",
        "tokens_minted": 10,
        "bag_id": "test-bag-001"
    }

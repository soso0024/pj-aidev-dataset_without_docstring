import pytest
import sys
import os

# Add project root to Python path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Global fixtures that can be used across test modules
@pytest.fixture
def sample_user_data():
    return {"id": 1, "name": "TestUser", "balance": 100.0, "password": "password123"}


@pytest.fixture
def sample_order_data():
    return {"user_id": 1, "amount": 50.0}

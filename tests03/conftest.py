import pytest
from repository.user_repo import _user_store
from repository.order_repo import _order_store


@pytest.fixture(autouse=True)
def reset_stores():
    """Reset all data stores before and after each test."""
    _user_store.clear()
    _order_store.clear()
    yield
    _user_store.clear()
    _order_store.clear()

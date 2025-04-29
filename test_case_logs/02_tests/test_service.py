import pytest
from model.user import User
from repository.user_repo import _user_store
from repository.order_repo import _order_store
from service.auth import register_user, authenticate
from service.payment import make_payment


@pytest.fixture(autouse=True)
def clear_stores():
    _user_store.clear()
    _order_store.clear()
    yield


def test_register_user_new():
    user = register_user(1, "TestUser", "password123", 100.0)
    assert user.id == 1
    assert user.name == "TestUser"
    assert user.balance == 100.0
    assert hasattr(user, "hashed_password")
    assert 1 in _user_store


def test_register_user_existing():
    existing = User(id=1, name="OldName", balance=50.0)
    _user_store[1] = existing
    user = register_user(1, "NewName", "password123")
    assert user.id == 1
    assert user.name == "NewName"
    assert user.balance == 50.0  # Balance preserved
    assert hasattr(user, "hashed_password")


def test_authenticate_success():
    user = register_user(1, "TestUser", "password123", 100.0)
    assert authenticate(1, "password123") is True


def test_authenticate_wrong_password():
    user = register_user(1, "TestUser", "password123", 100.0)
    assert authenticate(1, "wrongpassword") is False


def test_authenticate_user_not_exists():
    assert authenticate(99, "password123") is False


def test_make_payment_success():
    user = register_user(1, "TestUser", "password123", 100.0)
    new_balance = make_payment(1, 50.0)
    assert new_balance == 50.0
    assert _user_store[1].balance == 50.0
    assert len(_order_store) == 1
    assert _order_store[0].user_id == 1
    assert _order_store[0].amount == 50.0


def test_make_payment_insufficient_funds():
    user = register_user(1, "TestUser", "password123", 30.0)
    with pytest.raises(ValueError, match="Insufficient funds"):
        make_payment(1, 50.0)
    assert _user_store[1].balance == 30.0
    assert len(_order_store) == 0


def test_make_payment_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        make_payment(99, 50.0)

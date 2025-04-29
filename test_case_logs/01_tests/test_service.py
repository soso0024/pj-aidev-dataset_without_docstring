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


def test_register_new_user():
    user = register_user(1, "TestUser", "password123", 100.0)
    assert user.id == 1
    assert user.name == "TestUser"
    assert user.balance == 100.0
    assert hasattr(user, "hashed_password")
    assert user is _user_store.get(1)


def test_register_existing_user():
    existing_user = User(id=1, name="ExistingUser", balance=200.0)
    _user_store[1] = existing_user

    user = register_user(1, "UpdatedName", "newpassword", 50.0)
    assert user.id == 1
    assert user.name == "UpdatedName"
    assert user.balance == 200.0  # Balance should remain the same


def test_authenticate_success():
    register_user(1, "TestUser", "password123")
    result = authenticate(1, "password123")
    assert result is True


def test_authenticate_wrong_password():
    register_user(1, "TestUser", "password123")
    result = authenticate(1, "wrongpassword")
    assert result is False


def test_authenticate_nonexistent_user():
    result = authenticate(999, "password123")
    assert result is False


def test_make_payment_success():
    user = User(id=1, name="TestUser", balance=100.0)
    _user_store[1] = user

    remaining_balance = make_payment(1, 50.0)
    assert remaining_balance == 50.0
    assert user.balance == 50.0
    assert len(_order_store) == 1
    assert _order_store[0].user_id == 1
    assert _order_store[0].amount == 50.0


def test_make_payment_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        make_payment(999, 50.0)


def test_make_payment_insufficient_funds():
    user = User(id=1, name="TestUser", balance=20.0)
    _user_store[1] = user

    with pytest.raises(ValueError, match="Insufficient funds"):
        make_payment(1, 50.0)
    assert user.balance == 20.0
    assert len(_order_store) == 0

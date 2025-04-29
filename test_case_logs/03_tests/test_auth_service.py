import pytest
from service.auth import register_user, authenticate
from repository.user_repo import _user_store, get_user
from utils.string_utils import hash_password


@pytest.fixture
def clear_user_store():
    _user_store.clear()
    yield
    _user_store.clear()


def test_register_new_user(clear_user_store):
    user = register_user(1, "Test User", "password123", 100.0)
    assert user.id == 1
    assert user.name == "Test User"
    assert user.balance == 100.0
    assert hasattr(user, "hashed_password")
    assert user.hashed_password == hash_password("password123")
    assert get_user(1) is user


def test_register_existing_user(clear_user_store):
    user1 = register_user(1, "Test User", "password123", 100.0)
    user2 = register_user(1, "Updated User", "newpassword", 200.0)

    assert user2.id == 1
    assert user2.name == "Updated User"
    assert user2.balance == 100.0  # Balance should not change
    assert user2.hashed_password == hash_password("newpassword")
    assert get_user(1) is user2


def test_register_user_no_balance(clear_user_store):
    user = register_user(1, "Test User", "password123")
    assert user.balance == 0.0


def test_authenticate_success(clear_user_store):
    register_user(1, "Test User", "password123", 100.0)
    assert authenticate(1, "password123") is True


def test_authenticate_wrong_password(clear_user_store):
    register_user(1, "Test User", "password123", 100.0)
    assert authenticate(1, "wrongpassword") is False


def test_authenticate_nonexistent_user(clear_user_store):
    assert authenticate(999, "password123") is False

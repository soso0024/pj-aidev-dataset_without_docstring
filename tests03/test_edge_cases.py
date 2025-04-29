import pytest
from model.user import User
from service.payment import make_payment
from repository.user_repo import save_user
from repository.order_repo import _order_store


def test_payment_exact_balance():
    user = User(id=1, name="Test User", balance=50.0)
    save_user(user)

    new_balance = make_payment(1, 50.0)

    assert new_balance == 0.0
    assert user.balance == 0.0
    assert len(_order_store) == 1
    assert _order_store[0].user_id == 1
    assert _order_store[0].amount == 50.0


def test_payment_zero_amount():
    user = User(id=1, name="Test User", balance=50.0)
    save_user(user)

    new_balance = make_payment(1, 0.0)

    assert new_balance == 50.0
    assert user.balance == 50.0
    assert len(_order_store) == 1
    assert _order_store[0].amount == 0.0


def test_user_credit_negative_amount():
    user = User(id=1, name="Test User", balance=50.0)

    new_balance = user.credit(-10.0)

    assert new_balance == 40.0
    assert user.balance == 40.0


def test_hash_password_special_chars():
    from utils.string_utils import hash_password

    result = hash_password("p@$$w0rd!#")

    assert isinstance(result, str)
    assert len(result) == 64  # SHA-256 produces 64 character hex string

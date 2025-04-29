import pytest
from service.payment import make_payment
from repository.user_repo import _user_store, save_user
from repository.order_repo import _order_store
from model.user import User


@pytest.fixture
def clear_stores():
    _user_store.clear()
    _order_store.clear()
    yield
    _user_store.clear()
    _order_store.clear()


def test_make_payment_success(clear_stores):
    user = User(id=1, name="Test User", balance=100.0)
    save_user(user)

    new_balance = make_payment(1, 50.0)

    assert new_balance == 50.0
    assert user.balance == 50.0
    assert len(_order_store) == 1
    assert _order_store[0].user_id == 1
    assert _order_store[0].amount == 50.0


def test_make_payment_user_not_found(clear_stores):
    with pytest.raises(ValueError, match="User not found"):
        make_payment(999, 50.0)


def test_make_payment_insufficient_funds(clear_stores):
    user = User(id=1, name="Test User", balance=30.0)
    save_user(user)

    with pytest.raises(ValueError, match="Insufficient funds"):
        make_payment(1, 50.0)

    assert user.balance == 30.0
    assert len(_order_store) == 0

import pytest
from unittest.mock import patch
from data.generator import generate_users, generate_orders
from model.user import User
from model.order import Order


def test_generate_users():
    users = generate_users(3)
    assert len(users) == 3
    for i, user in enumerate(users, 1):
        assert user.id == i
        assert user.name == f"User{i}"
        assert user.balance >= 10.0
        assert user.balance <= 100.0


@patch("random.uniform")
@patch("random.randint")
def test_generate_orders(mock_randint, mock_uniform):
    mock_randint.return_value = 2
    mock_uniform.return_value = 10.0

    users = [
        User(id=1, name="User1", balance=50.0),
        User(id=2, name="User2", balance=30.0),
    ]

    orders = generate_orders(users, max_orders=2)

    assert len(orders) == 4  # 2 users with 2 orders each
    assert all(isinstance(order, Order) for order in orders)
    assert all(order.amount == 10.0 for order in orders)
    assert [order.user_id for order in orders] == [1, 1, 2, 2]


@patch("random.uniform")
@patch("random.randint")
def test_generate_orders_insufficient_balance(mock_randint, mock_uniform):
    # First user will make 3 orders (if possible)
    mock_randint.return_value = 3

    # First order will use 0.9 of the balance, leaving only 0.1 (less than threshold of 1)
    mock_uniform.side_effect = lambda min_val, max_val: 0.9

    users = [User(id=1, name="User1", balance=1.0)]

    with patch("builtins.print") as mock_print:
        orders = generate_orders(users, max_orders=3)

        # No orders should be created because the balance check happens before order creation
        assert len(orders) == 0

        # Verify the print statement about skipping was called
        mock_print.assert_any_call(
            "Skipping order generation due to insufficient balance."
        )

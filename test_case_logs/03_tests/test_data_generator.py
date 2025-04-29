import pytest
from unittest.mock import patch
from data.generator import generate_users, generate_orders
from model.user import User
from model.order import Order


def test_generate_users():
    users = generate_users(3)
    assert len(users) == 3
    assert all(isinstance(u, User) for u in users)
    assert [u.id for u in users] == [1, 2, 3]
    assert [u.name for u in users] == ["User1", "User2", "User3"]
    assert all(10 <= u.balance <= 100 for u in users)


@patch("random.uniform")
@patch("random.randint")
def test_generate_orders(mock_randint, mock_uniform):
    mock_randint.return_value = 2
    # Need 4 values: 2 users * 2 orders each = 4 values needed
    mock_uniform.side_effect = [20.0, 10.0, 15.0, 5.0]

    users = [
        User(id=1, name="User1", balance=50.0),
        User(id=2, name="User2", balance=30.0),
    ]

    orders = generate_orders(users, max_orders=3)

    assert len(orders) == 4  # 2 orders per user (2 users * 2 orders)
    assert all(isinstance(o, Order) for o in orders)
    assert orders[0].user_id == 1
    assert orders[1].user_id == 1
    assert orders[2].user_id == 2
    assert orders[3].user_id == 2


def test_orders_with_insufficient_balance():
    # Create a user with balance just at threshold (1.0) so we don't create any orders
    user = User(id=1, name="User1", balance=1.0)

    # Directly test with print message
    with patch("builtins.print") as mock_print:
        orders = generate_orders([user], max_orders=2)

        # We expect no orders to be created with balance 1.0 (at threshold)
        assert len(orders) == 0
        mock_print.assert_any_call(
            "Skipping order generation due to insufficient balance."
        )

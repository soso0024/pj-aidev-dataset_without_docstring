import pytest
from unittest.mock import patch, call
from model.user import User
from model.order import Order
from data.generator import generate_users, generate_orders


def test_generate_users():
    users = generate_users(5)
    assert len(users) == 5
    for i, user in enumerate(users, 1):
        assert user.id == i
        assert user.name == f"User{i}"
        assert 10 <= user.balance <= 100


def test_generate_users_zero():
    users = generate_users(0)
    assert users == []


@patch("random.uniform")
@patch("random.randint")
def test_generate_orders_normal(mock_randint, mock_uniform):
    # Set up mocks
    mock_randint.return_value = 2  # Each user gets 2 orders
    # Need enough values for all calls to uniform()
    mock_uniform.side_effect = [20.0, 10.0, 15.0, 5.0]

    # Create test users
    users = [
        User(id=1, name="User1", balance=50.0),
        User(id=2, name="User2", balance=30.0),
    ]

    orders = generate_orders(users, max_orders=3)

    assert len(orders) == 4  # 2 users × 2 orders each

    # Check user IDs and order amounts
    assert orders[0].user_id == 1
    assert orders[1].user_id == 1
    assert orders[2].user_id == 2
    assert orders[3].user_id == 2


@patch("builtins.print")
@patch("random.uniform")
@patch("random.randint")
def test_generate_orders_insufficient_balance(mock_randint, mock_uniform, mock_print):
    # Set up mocks
    mock_randint.return_value = 3  # Try to generate 3 orders
    # First value is > 0.9 (user balance) so it'll skip
    mock_uniform.side_effect = [2.0, 0.5]

    # Create test user with low balance
    users = [User(id=1, name="User1", balance=0.9)]

    orders = generate_orders(users, max_orders=3)

    # Should skip due to insufficient balance
    assert len(orders) == 0
    mock_print.assert_any_call("Skipping order generation due to insufficient balance.")


def test_generate_orders_empty_users():
    orders = generate_orders([])
    assert orders == []

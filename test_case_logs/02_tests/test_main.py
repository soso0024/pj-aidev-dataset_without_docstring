import pytest
from unittest.mock import patch, MagicMock
import main
from config.settings import APP_NAME


@patch("main.print")
@patch("main.make_payment")
@patch("main.authenticate")
@patch("main.register_user")
@patch("main.generate_orders")
@patch("main.generate_users")
def test_run_demo(
    mock_gen_users, mock_gen_orders, mock_register, mock_auth, mock_payment, mock_print
):
    # Mock user generation
    user1 = MagicMock()
    user1.id = 1
    user1.name = "User1"
    user1.balance = 50.0

    user2 = MagicMock()
    user2.id = 2
    user2.name = "User2"
    user2.balance = 30.0

    users = [user1, user2]
    mock_gen_users.return_value = users

    # Mock order generation
    order1 = MagicMock()
    order1.user_id = 1
    order1.amount = 20.0
    order1.summary.return_value = "Order for user 1: $20.00 at timestamp"

    order2 = MagicMock()
    order2.user_id = 2
    order2.amount = 10.0
    order2.summary.return_value = "Order for user 2: $10.00 at timestamp"

    orders = [order1, order2]
    mock_gen_orders.return_value = orders

    # Mock authentication
    mock_auth.return_value = True

    # Mock payment
    mock_payment.side_effect = [30.0, 20.0]

    # Run the demo function
    main.run_demo()

    # Verify function calls
    mock_gen_users.assert_called_once_with(5)
    mock_gen_orders.assert_called_once_with(users)

    # Verify user registration calls
    assert mock_register.call_count == 2
    mock_register.assert_any_call(1, "User1", "pass123", 50.0)
    mock_register.assert_any_call(2, "User2", "pass123", 30.0)

    # Verify authentication call
    mock_auth.assert_called_once_with(1, "pass123")

    # Verify payment calls
    assert mock_payment.call_count == 2
    mock_payment.assert_any_call(1, 20.0)
    mock_payment.assert_any_call(2, 10.0)

    # Verify print calls
    expected_app_name = f"{APP_NAME} v{__import__('config').settings.VERSION}"
    mock_print.assert_any_call(f"{expected_app_name} starting...")
    mock_print.assert_any_call("Authentication successful for User1")
    mock_print.assert_any_call(
        f"Processed Order for user 1: $20.00 at timestamp, remaining balance: 30.00"
    )
    mock_print.assert_any_call(
        f"Processed Order for user 2: $10.00 at timestamp, remaining balance: 20.00"
    )
    mock_print.assert_any_call("Demo complete.")

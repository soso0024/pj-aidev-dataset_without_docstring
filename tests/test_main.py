import pytest
from unittest.mock import patch, MagicMock, call
import main
from config.settings import APP_NAME, VERSION


@patch("main.make_payment")
@patch("main.authenticate")
@patch("main.register_user")
@patch("main.generate_orders")
@patch("main.generate_users")
@patch("builtins.print")
def test_run_demo(
    mock_print, mock_gen_users, mock_gen_orders, mock_register, mock_auth, mock_payment
):
    # Setup mocks
    mock_users = [
        MagicMock(id=1, name="User1", balance=50.0),
        MagicMock(id=2, name="User2", balance=30.0),
    ]
    mock_gen_users.return_value = mock_users

    mock_orders = [
        MagicMock(user_id=1, amount=10.0, summary=lambda: "Order1 summary"),
        MagicMock(user_id=2, amount=15.0, summary=lambda: "Order2 summary"),
    ]
    mock_gen_orders.return_value = mock_orders

    mock_auth.return_value = True
    mock_payment.side_effect = [40.0, 15.0]

    # Run the demo
    main.run_demo()

    # Verify interactions
    assert mock_gen_users.call_count == 1
    assert mock_gen_users.call_args[0][0] == 5

    assert mock_register.call_count == len(mock_users)
    for i, user in enumerate(mock_users):
        assert mock_register.call_args_list[i][0][:3] == (user.id, user.name, "pass123")

    assert mock_auth.call_count == 1
    assert mock_auth.call_args[0] == (1, "pass123")

    assert mock_gen_orders.call_count == 1
    assert mock_gen_orders.call_args[0][0] == mock_users

    assert mock_payment.call_count == len(mock_orders)
    for i, order in enumerate(mock_orders):
        assert mock_payment.call_args_list[i][0] == (order.user_id, order.amount)

    # Check that the demo messages were printed
    app_version_call = f"{APP_NAME} v{VERSION} starting..."
    assert mock_print.call_args_list[0][0][0].startswith(app_version_call)
    assert mock_print.call_args_list[1][0][0] == "Authentication successful for User1"
    mock_print.assert_has_calls([call("Demo complete.")], any_order=True)

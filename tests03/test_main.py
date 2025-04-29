import pytest
from unittest.mock import patch, call, Mock, ANY
import main
import importlib
from config.settings import APP_NAME, VERSION, DEBUG


def test_config_values():
    assert APP_NAME == "TestApp"
    assert VERSION == "0.1.0"
    assert DEBUG is True


def test_run_demo():
    # Use context managers for all mocks
    with patch("builtins.print") as mock_print:
        with patch("config.settings.VERSION", "0.1.0"):
            with patch("data.generator.generate_users") as mock_gen_users:
                with patch("data.generator.generate_orders") as mock_gen_orders:
                    with patch("service.auth.register_user") as mock_register:
                        with patch("service.auth.authenticate") as mock_auth:
                            with patch("service.payment.make_payment") as mock_payment:
                                # Setup mocks
                                user1 = Mock()
                                user1.id = 1
                                user1.name = "User1"
                                user1.balance = 50.0

                                user2 = Mock()
                                user2.id = 2
                                user2.name = "User2"
                                user2.balance = 60.0

                                users = [user1, user2]

                                order1 = Mock()
                                order1.user_id = 1
                                order1.amount = 20.0
                                order1.summary.return_value = (
                                    "Order for user 1: $20.00 at 2023-01-01T00:00:00"
                                )

                                order2 = Mock()
                                order2.user_id = 2
                                order2.amount = 30.0
                                order2.summary.return_value = (
                                    "Order for user 2: $30.00 at 2023-01-01T00:00:00"
                                )

                                orders = [order1, order2]

                                mock_gen_users.return_value = users
                                mock_gen_orders.return_value = orders
                                mock_auth.return_value = True
                                mock_payment.side_effect = [30.0, 30.0]

                                # Need to reload main module after setting up patches
                                importlib.reload(main)

                                # Run the function
                                main.run_demo()

                                # Assert functions were called correctly
                                mock_gen_users.assert_called_once_with(5)
                                mock_gen_orders.assert_called_once_with(users)

                                # Use ANY for the name since it's a Mock
                                assert mock_register.call_count == 2
                                mock_register.assert_any_call(
                                    1, "User1", "pass123", 50.0
                                )
                                mock_register.assert_any_call(
                                    2, "User2", "pass123", 60.0
                                )

                                mock_auth.assert_called_once_with(1, "pass123")

                                assert mock_payment.call_count == 2
                                mock_payment.assert_has_calls(
                                    [call(1, 20.0), call(2, 30.0)]
                                )

                                # Check print calls
                                mock_print.assert_any_call(
                                    f"{APP_NAME} v{VERSION} starting..."
                                )
                                mock_print.assert_any_call(
                                    "Authentication successful for User1"
                                )
                                mock_print.assert_any_call(
                                    "Processed Order for user 1: $20.00 at 2023-01-01T00:00:00, remaining balance: 30.00"
                                )
                                mock_print.assert_any_call(
                                    "Processed Order for user 2: $30.00 at 2023-01-01T00:00:00, remaining balance: 30.00"
                                )
                                mock_print.assert_any_call("Demo complete.")

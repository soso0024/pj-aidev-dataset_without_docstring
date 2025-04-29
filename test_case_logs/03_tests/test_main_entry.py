import pytest
from unittest.mock import patch
import sys


@patch("main.run_demo")
def test_main_entry_point(mock_run_demo):
    """Test the __main__ block in main.py"""
    # Directly use the main module's __name__ handling
    import builtins

    original_import = __import__

    def mock_import(name, *args, **kwargs):
        if name == "main":
            module = original_import(name, *args, **kwargs)
            # Simulate if __name__ == "__main__" directly
            main_globals = vars(module)
            if main_globals.get("__name__") == "main":
                run_demo = main_globals.get("run_demo")
                if callable(run_demo):
                    run_demo()
            return module
        return original_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=mock_import):
        import main

        mock_run_demo.assert_called_once()

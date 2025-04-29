import pytest
from utils.string_utils import hash_password, to_upper
from utils.math_utils import add, multiply, safe_divide


def test_hash_password():
    hashed = hash_password("password123")
    assert isinstance(hashed, str)
    assert len(hashed) == 64
    assert hash_password("password123") == hash_password("password123")
    assert hash_password("password123") != hash_password("password124")


def test_to_upper():
    assert to_upper("test") == "TEST"
    assert to_upper("Test String") == "TEST STRING"
    assert to_upper("") == ""


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0
    assert multiply(1.5, 2) == 3.0


def test_safe_divide_normal():
    assert safe_divide(6, 3) == 2
    assert safe_divide(5, 2) == 2.5
    assert safe_divide(0, 5) == 0


def test_safe_divide_by_zero():
    assert safe_divide(5, 0) is None

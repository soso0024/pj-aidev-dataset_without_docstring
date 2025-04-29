import pytest
from utils.math_utils import add, multiply, safe_divide
from utils.string_utils import hash_password, to_upper


def test_add():
    assert add(5, 3) == 8
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_multiply():
    assert multiply(5, 3) == 15
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0


def test_safe_divide_normal():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 2) == 3.5
    assert safe_divide(0, 5) == 0.0


def test_safe_divide_by_zero():
    assert safe_divide(10, 0) is None


def test_hash_password():
    hashed = hash_password("password123")
    expected = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
    assert hashed == expected
    assert (
        hash_password("")
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_to_upper():
    assert to_upper("hello") == "HELLO"
    assert to_upper("Hello World") == "HELLO WORLD"
    assert to_upper("123") == "123"
    assert to_upper("") == ""

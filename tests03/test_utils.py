import pytest
from utils.math_utils import add, multiply, safe_divide
from utils.string_utils import hash_password, to_upper


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0


def test_safe_divide():
    assert safe_divide(10, 2) == 5
    assert safe_divide(7, 2) == 3.5
    assert safe_divide(5, 0) is None


def test_hash_password():
    assert (
        hash_password("password")
        == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    )
    assert (
        hash_password("")
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert hash_password("password") == hash_password("password")
    assert hash_password("password") != hash_password("Password")


def test_to_upper():
    assert to_upper("hello") == "HELLO"
    assert to_upper("Hello World") == "HELLO WORLD"
    assert to_upper("123") == "123"
    assert to_upper("") == ""

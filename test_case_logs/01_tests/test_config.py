import pytest
from config import settings


def test_settings_values():
    assert settings.APP_NAME == "TestApp"
    assert settings.VERSION == "0.1.0"
    assert settings.DEBUG == True

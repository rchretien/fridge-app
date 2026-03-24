"""Test Fridge App backend."""

import fridge_app_backend


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(fridge_app_backend.__name__, str)

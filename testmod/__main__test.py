"""Tests for __main__"""

from . import __main__ as main


def test_test_fn() -> None:
    """Ensure the function returns 1"""
    assert main.test_fn() == 1  # nosec

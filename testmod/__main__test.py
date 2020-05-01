from . import __main__ as main


def test_test_fn():
    assert main.test_fn() == 1  # nosec

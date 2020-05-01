""" This is a test module for testing compiling """

import sys


def test_fn() -> int:
    """This function tests returning"""

    print("fn run")
    return 1


if __name__ == "__main__":
    print("The module has run")
    print("result: " + str(test_fn()))

    sys.exit(0)

import pytest
from src.ipm_functions import add

class TestOriginalDummy:
    """
    Tests mirroring the logic from test_cov_dummy.c.
    """

    def test_add_positive_numbers(self):
        """
        Original test: check add(1, 2) == 3.
        """
        assert add(1, 2) == 3, "Test failed: add(1, 2) != 3"

    def test_add_negative_and_positive_numbers(self):
        """
        Original test: check add(-2, 5) == 3.
        """
        assert add(-2, 5) == 3, "Test failed: add(-2, 5) != 3"

    def test_add_zeros(self):
        """
        Original test: check add(0, 0) == 0.
        """
        assert add(0, 0) == 0, "Test failed: add(0, 0) != 0"
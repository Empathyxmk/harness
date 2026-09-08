import pytest
from src.ipm_functions import add

class TestPublicDummy:
    """
    Tests mirroring the logic from test_cov_dummy_public.c.
    """

    def test_public_add_positive_numbers(self):
        """
        Public test: check add(2, 4) == 6.
        """
        assert add(2, 4) == 6, "Public Test failed: add(2, 4) != 6"

    def test_public_add_negative_and_positive_numbers(self):
        """
        Public test: check add(-5, 8) == 3.
        """
        assert add(-5, 8) == 3, "Public Test failed: add(-5, 8) != 3"

    def test_public_add_to_zero(self):
        """
        Public test: check add(10, -10) == 0.
        """
        assert add(10, -10) == 0, "Public Test failed: add(10, -10) != 0"
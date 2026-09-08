import pytest
from switchml.common import add

class TestUtilsPublic:
    def test_add_positive_numbers(self):
        assert add(7, 8) == 15

    def test_add_negative_numbers(self):
        assert add(-6, -4) == -10

    def test_add_zero(self):
        assert add(0, 12) == 12
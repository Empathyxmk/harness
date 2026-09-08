import pytest
from src.sample import add, max

class TestAdd:
    def test_adds_two_positive_numbers(self):
        assert add(2, 4) == 6

    def test_adds_a_negative_and_positive_number(self):
        assert add(-5, 3) == -2

    def test_adds_two_zeros(self):
        assert add(0, 0) == 0

class TestMax:
    def test_maximum_in_positive_array(self):
        assert max([1, 3, 2]) == 3

    def test_maximum_in_negative_array(self):
        assert max([-1, -3, -2]) == -1

    def test_returns_none_for_empty_array(self):
        assert max([]) is None

    def test_returns_none_for_undefined(self):
        assert max(None) is None

    def test_returns_value_for_single_element_array(self):
        assert max([42]) == 42
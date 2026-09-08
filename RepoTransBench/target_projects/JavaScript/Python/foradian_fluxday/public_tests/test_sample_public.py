import pytest
from src.sample import add, max

class TestAdd:
    def test_adds_two_positive_numbers(self):
        assert add(7, 10) == 17

    def test_adds_a_negative_and_positive_number(self):
        assert add(-8, 4) == -4

    def test_adds_two_zeros(self):
        assert add(0, 0) == 0

class TestMax:
    def test_maximum_in_positive_array(self):
        assert max([5, 8, 7]) == 8

    def test_maximum_in_negative_array(self):
        assert max([-10, -5, -8]) == -5

    def test_returns_none_for_empty_array(self):
        assert max([]) is None

    def test_returns_none_for_undefined(self):
        assert max(None) is None

    def test_returns_value_for_single_element_array(self):
        assert max([99]) == 99
import pytest
from src.utils import add, max, isEven, greet

class TestAdd:
    def test_adds_positives(self):
        assert add(4, 7) == 11

    def test_adds_negatives(self):
        assert add(-6, -1) == -7

class TestMax:
    def test_returns_first_if_greater(self):
        assert max(15, 4) == 15

    def test_returns_second_if_greater(self):
        assert max(5, 12) == 12

    def test_returns_either_if_equal(self):
        assert max(20, 20) in [20, 20]

class TestIsEven:
    def test_true_for_even_numbers(self):
        assert isEven(10) is True

    def test_false_for_odd_numbers(self):
        assert isEven(11) is False

    def test_throws_for_non_number(self):
        with pytest.raises(ValueError, match="Input must be a number"):
            isEven(None)

class TestGreet:
    def test_greets_by_name(self):
        assert greet("Alex") == "Hello, Alex!"

    def test_greets_world_if_no_name(self):
        assert greet() == "Hello, world!"

    def test_greets_world_for_falsy_name(self):
        assert greet(0) == "Hello, world!"
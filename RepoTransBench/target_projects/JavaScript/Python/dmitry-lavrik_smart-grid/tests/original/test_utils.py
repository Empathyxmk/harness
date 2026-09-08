import pytest
from src.utils import add, max, isEven, greet

class TestAdd:
    def test_adds_positives(self):
        assert add(2, 3) == 5

    def test_adds_negatives(self):
        assert add(-2, -5) == -7

class TestMax:
    def test_returns_first_if_greater(self):
        assert max(10, 2) == 10

    def test_returns_second_if_greater(self):
        assert max(3, 9) == 9

    def test_returns_either_if_equal(self):
        assert max(7, 7) in [7, 7]

class TestIsEven:
    def test_true_for_even_numbers(self):
        assert isEven(4) is True

    def test_false_for_odd_numbers(self):
        assert isEven(7) is False

    def test_throws_for_non_number(self):
        with pytest.raises(ValueError, match="Input must be a number"):
            isEven("str")

class TestGreet:
    def test_greets_by_name(self):
        assert greet("Dmitry") == "Hello, Dmitry!"

    def test_greets_world_if_no_name(self):
        assert greet() == "Hello, world!"

    def test_greets_world_for_falsy_name(self):
        assert greet("") == "Hello, world!"
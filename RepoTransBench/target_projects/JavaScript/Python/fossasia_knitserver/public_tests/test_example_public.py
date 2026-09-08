import math
import pytest

from src.example import add, subtract, isPositive, classify

class TestAddPublic:
    def test_adds_positive_numbers(self):
        assert add(10, 3) == 13

    def test_adds_negative_numbers(self):
        assert add(-3, -5) == -8

class TestSubtractPublic:
    def test_subtracts_numbers(self):
        assert subtract(8, 3) == 5

    def test_throws_error_on_invalid_arguments(self):
        with pytest.raises(ValueError, match="Invalid arguments"):
            subtract({}, 2)

class TestIsPositivePublic:
    def test_returns_true_for_positive_number(self):
        assert isPositive(42) is True

    def test_returns_false_for_zero(self):
        assert isPositive(0) is False

    def test_returns_false_for_negative(self):
        assert isPositive(-99) is False

    def test_returns_false_for_non_number(self):
        assert isPositive([1,2,3]) is False

class TestClassifyPublic:
    def test_returns_positive_for_gt_zero(self):
        assert classify(99) == "positive"

    def test_returns_negative_for_lt_zero(self):
        assert classify(-100) == "negative"

    def test_returns_zero_for_zero(self):
        assert classify(0) == "zero"

    def test_returns_not_a_number_for_nan(self):
        # The JS test uses classify(undefined), which
        # in Python should be a completely invalid input.
        # We'll simulate by passing None
        assert classify(None) == "not a number"
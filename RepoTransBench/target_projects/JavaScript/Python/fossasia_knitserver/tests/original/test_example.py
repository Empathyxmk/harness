import math
import pytest

from src.example import add, subtract, isPositive, classify

class TestAdd:
    def test_adds_positive_numbers(self):
        assert add(1, 2) == 3

    def test_adds_negative_numbers(self):
        assert add(-1, -1) == -2

class TestSubtract:
    def test_subtracts_numbers(self):
        assert subtract(5, 1) == 4

    def test_throws_error_on_invalid_arguments(self):
        with pytest.raises(ValueError, match="Invalid arguments"):
            subtract("a", 2)

class TestIsPositive:
    def test_returns_true_for_positive_number(self):
        assert isPositive(3) is True

    def test_returns_false_for_zero(self):
        assert isPositive(0) is False

    def test_returns_false_for_negative(self):
        assert isPositive(-10) is False

    def test_returns_false_for_non_number(self):
        assert isPositive("str") is False

class TestClassify:
    def test_returns_positive_for_gt_zero(self):
        assert classify(5) == "positive"

    def test_returns_negative_for_lt_zero(self):
        assert classify(-2) == "negative"

    def test_returns_zero_for_zero(self):
        assert classify(0) == "zero"

    def test_returns_not_a_number_for_nan(self):
        assert classify(float('nan')) == "not a number"
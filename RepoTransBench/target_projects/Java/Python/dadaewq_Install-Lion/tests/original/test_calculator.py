import pytest
from src.calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add(self):
        assert self.calculator.add(2, 3) == 5
        assert self.calculator.add(2, -3) == -1

    def test_subtract(self):
        assert self.calculator.subtract(2, 3) == -1
        assert self.calculator.subtract(2, -3) == 5

    def test_multiply(self):
        assert self.calculator.multiply(2, 3) == 6
        assert self.calculator.multiply(2, -3) == -6

    def test_divide(self):
        assert self.calculator.divide(6, 3) == 2
        assert self.calculator.divide(6, -3) == -2

    def test_divide_by_zero(self):
        with pytest.raises(ValueError) as exc_info:
            self.calculator.divide(1, 0)
        assert str(exc_info.value) == "Divider cannot be zero."
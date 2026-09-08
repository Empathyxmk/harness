import pytest
from src.calculator import Calculator

class TestCalculatorPublic:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add(self):
        assert self.calculator.add(4, 7) == 11
        assert self.calculator.add(6, -3) == 3

    def test_subtract(self):
        assert self.calculator.subtract(10, 2) == 8
        assert self.calculator.subtract(9, -3) == 12

    def test_multiply(self):
        assert self.calculator.multiply(5, 7) == 35
        assert self.calculator.multiply(4, -5) == -20

    def test_divide(self):
        assert self.calculator.divide(72, 8) == 9
        assert self.calculator.divide(12, -3) == -4

    def test_divide_by_zero(self):
        with pytest.raises(ValueError) as exc_info:
            self.calculator.divide(8, 0)
        assert str(exc_info.value) == "Divider cannot be zero."
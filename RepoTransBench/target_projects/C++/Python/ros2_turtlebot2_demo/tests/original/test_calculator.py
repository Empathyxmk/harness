import pytest
from src.calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_addition(self):
        assert self.calc.add(2, 2) == 4
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0

    def test_subtraction(self):
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(3, 5) == -2
        assert self.calc.subtract(0, 0) == 0

    def test_multiplication(self):
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(-2, 5) == -10
        assert self.calc.multiply(0, 100) == 0

    def test_division(self):
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(5, 2) == 2  # Integer division
        assert self.calc.divide(-10, 2) == -5

    def test_division_by_zero(self):
        with pytest.raises(RuntimeError):
            self.calc.divide(10, 0)

def test_constructor_works():
    c = Calculator()
    assert c is not None
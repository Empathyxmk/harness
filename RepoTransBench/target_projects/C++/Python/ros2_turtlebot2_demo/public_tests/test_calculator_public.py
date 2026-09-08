import pytest
from src.calculator import Calculator

class TestCalculatorPublic:
    def setup_method(self):
        self.calc = Calculator()

    def test_addition(self):
        assert self.calc.add(100, 23) == 123
        assert self.calc.add(-5, -7) == -12
        assert self.calc.add(1, 0) == 1

    def test_subtraction(self):
        assert self.calc.subtract(100, 80) == 20
        assert self.calc.subtract(-20, 7) == -27
        assert self.calc.subtract(45, 45) == 0

    def test_multiplication(self):
        assert self.calc.multiply(7, 8) == 56
        assert self.calc.multiply(-3, 6) == -18
        assert self.calc.multiply(42, 0) == 0

    def test_division(self):
        assert self.calc.divide(81, 3) == 27
        assert self.calc.divide(8, 3) == 2  # Integer division, 8/3 = 2.x
        assert self.calc.divide(-21, 7) == -3

    def test_division_by_zero(self):
        with pytest.raises(RuntimeError):
            self.calc.divide(-15, 0)

def test_constructor_works():
    c = Calculator()
    assert c is not None
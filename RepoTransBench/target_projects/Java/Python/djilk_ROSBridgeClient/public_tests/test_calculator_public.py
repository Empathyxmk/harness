import pytest

from src.calculator import Calculator

class TestCalculatorPublic:
    def test_add(self):
        calc = Calculator()
        # Changed input from (2,3)=5 to (4,7)=11
        assert calc.add(4, 7) == 11

    def test_subtract(self):
        calc = Calculator()
        # Changed input from (5,3)=2 to (10,4)=6
        assert calc.subtract(10, 4) == 6

    def test_multiply(self):
        calc = Calculator()
        # Changed input from (2,3)=6 to (5,4)=20
        assert calc.multiply(5, 4) == 20

    def test_divide(self):
        calc = Calculator()
        # Changed input from (6,3)=2 to (20,4)=5
        assert calc.divide(20, 4) == 5

    def test_divide_by_zero(self):
        calc = Calculator()
        # Test checks divide by zero with numerator 17
        with pytest.raises(ValueError):
            calc.divide(17, 0)
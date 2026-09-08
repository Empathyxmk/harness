import pytest

# Dummy implementation of DemoCoverage for illustration
class DemoCoverage:
    def add(self, x, y):
        return x + y
    def isEven(self, val):
        return val % 2 == 0
    def divide(self, x, y):
        if y == 0:
            raise ArithmeticError("/ by zero")
        return x // y

def test_add_positive_numbers():
    demo = DemoCoverage()
    assert demo.add(2, 3) == 5

def test_add_negative_numbers():
    demo = DemoCoverage()
    assert demo.add(-2, -3) == -5

def test_iseven_even_number():
    demo = DemoCoverage()
    assert demo.isEven(4) is True

def test_iseven_odd_number():
    demo = DemoCoverage()
    assert demo.isEven(5) is False

def test_divide_regular_case():
    demo = DemoCoverage()
    assert demo.divide(6, 3) == 2

def test_divide_divide_by_zero():
    demo = DemoCoverage()
    with pytest.raises(ArithmeticError) as excinfo:
        demo.divide(10, 0)
    assert str(excinfo.value) == "/ by zero"
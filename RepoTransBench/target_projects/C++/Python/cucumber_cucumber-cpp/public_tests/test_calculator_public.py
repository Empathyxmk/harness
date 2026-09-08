import math
import pytest

# The Calculator class is assumed to be implemented elsewhere and imported.
# For demonstration, a minimal implementation is shown below,
# but for full validation, the real Calculator class must be provided.

class Calculator:
    def __init__(self):
        self.stack = []
    def push(self, val):
        self.stack.append(val)
    def add(self):
        return sum(self.stack) if self.stack else 0.0
    def divide(self):
        if not self.stack:
            return float("nan")
        result = self.stack[0]
        for val in self.stack[1:]:
            if val == 0:
                result = float("inf") if result != 0 else float("nan")
                break
            result /= val
        return result

def test_add_empty_stack_different():
    calc = Calculator()
    assert calc.add() == 0.0

def test_add_multiple_different():
    calc = Calculator()
    calc.push(4.0)
    calc.push(-1.0)
    calc.push(3.0)
    assert math.isclose(calc.add(), 6.0, abs_tol=1e-9)

def test_divide_empty_stack_different():
    calc = Calculator()
    result = calc.divide()
    assert math.isnan(result)

def test_divide_one_element_different():
    calc = Calculator()
    calc.push(-7.25)
    assert calc.divide() == -7.25
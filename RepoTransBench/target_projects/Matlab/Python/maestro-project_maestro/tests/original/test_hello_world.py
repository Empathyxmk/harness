import pytest

def test_sum():
    # Basic test to ensure test harness works
    act_solution = 2 + 2
    exp_solution = 4
    assert act_solution == exp_solution

def if_else_function(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

def test_if_else():
    # Branch coverage demo: Simple if-else
    assert if_else_function(3) == "positive"
    assert if_else_function(-1) == "negative"
    assert if_else_function(0) == "zero"

def test_for_loop():
    # Line coverage demo: Simple for loop
    s = 0
    for i in range(1, 6):
        s += i
    assert s == 15
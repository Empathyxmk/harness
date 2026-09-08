from src.math_operations import add, subtract, multiply, divide

def test_add():
    assert add(10, 20) == 30
    assert add(-5, 15) == 10
    assert add(-7, -3) == -10
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(40, 17) == 23
    assert subtract(-8, 15) == -23
    assert subtract(-20, -8) == -12
    assert subtract(0, 6) == -6

def test_multiply():
    assert multiply(3, 7) == 21
    assert multiply(-6, 3) == -18
    assert multiply(-4, -4) == 16
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(100, 4) == 25
    assert divide(-36, 6) == -6
    assert divide(-20, -5) == 4
    assert divide(15, 0) == 0
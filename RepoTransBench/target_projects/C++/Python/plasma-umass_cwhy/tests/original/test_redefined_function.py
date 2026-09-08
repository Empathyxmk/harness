def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def test_add():
    assert add(2, 3) == 5
    assert add(-5, 5) == 0

def test_subtract():
    assert subtract(10, 2) == 8
    assert subtract(-2, -5) == 3
def add(a, b):
    return a + b

def sub(a, b):
    if a > b:
        return a - b
    else:
        return b - a

def mul(a, b):
    return a * b

def div_safe(a, b):
    if b == 0:
        return 0
    return a // b

def test_add_public():
    assert add(10, 7) == 17
    assert add(-3, 1) == -2

def test_sub_public():
    assert sub(8, 4) == 4
    assert sub(2, 9) == 7

def test_mul_public():
    assert mul(5, 6) == 30
    assert mul(-2, 3) == -6

def test_div_safe_public():
    assert div_safe(15, 3) == 5
    assert div_safe(10, 0) == 0
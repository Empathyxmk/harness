from qcore.asserts import assert_eq

def add(x, y):
    return x + y

def test_public_add():
    assert_eq(add(10, 15), 25)
    assert_eq(add(-100, 80), -20)
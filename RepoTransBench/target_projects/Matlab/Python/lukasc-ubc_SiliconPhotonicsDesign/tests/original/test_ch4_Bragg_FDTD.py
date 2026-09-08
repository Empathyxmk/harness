def dummy_bragg(a, b):
    return a * b

def test_basic():
    y = dummy_bragg(2, 3)
    assert y == 6

def test_zero():
    y = dummy_bragg(2, 0)
    assert y == 0
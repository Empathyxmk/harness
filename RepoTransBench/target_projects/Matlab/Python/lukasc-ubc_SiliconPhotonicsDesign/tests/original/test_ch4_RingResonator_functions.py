def dummy_rr(a, b):
    return a + b

def test_rr():
    assert dummy_rr(2, 3) == 5

def test_rr_zero():
    assert dummy_rr(0, 0) == 0
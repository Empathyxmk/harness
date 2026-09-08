def dummy_dc_gds(a, b, c):
    return a * b * c

def test_basic():
    v = dummy_dc_gds(1, 2, 3)
    assert v == 6

def test_zero():
    v = dummy_dc_gds(1, 2, 0)
    assert v == 0
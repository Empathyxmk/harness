def dummy_1d(h, w):
    if w == 0:
        return float('inf')
    else:
        return h / w

def test_basic():
    y = dummy_1d(6, 2)
    assert y == 3

def test_zero_w():
    y = dummy_1d(6, 0)
    assert y == float('inf')
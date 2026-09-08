def dummy_2d_profile(h, w, n):
    if h == 0:
        return 0
    else:
        return h / w / n

def test_basic():
    out = dummy_2d_profile(6, 2, 1)
    assert out == 3

def test_zero_h():
    out = dummy_2d_profile(0, 2, 2)
    assert out == 0
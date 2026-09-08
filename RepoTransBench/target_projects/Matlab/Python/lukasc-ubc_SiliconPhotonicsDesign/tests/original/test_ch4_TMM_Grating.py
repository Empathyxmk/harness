def dummy_grating(a, b, n):
    return a * b * n

def test_basic():
    g = dummy_grating(4, 2, 1)
    assert g == 8

def test_neg_vals():
    g = dummy_grating(-2, 3, 5)
    assert g == -30
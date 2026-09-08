def dummy_grating_public(a, b, n):
    return a * b * n

def test_basic_public():
    g = dummy_grating_public(3, 7, 2)
    assert g == 42

def test_neg_vals_public():
    g = dummy_grating_public(-4, 2, 3)
    assert g == -24
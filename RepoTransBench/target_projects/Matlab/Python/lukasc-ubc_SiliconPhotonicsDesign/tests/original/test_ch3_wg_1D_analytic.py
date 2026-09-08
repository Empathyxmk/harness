def dummy_analytic(n1, n2, d):
    if d == 0:
        return float('inf')
    else:
        return (n1 - n2) / d

def test_basic():
    out = dummy_analytic(2, 2, 4)
    assert out == 0.0

def test_div_by_zero():
    out = dummy_analytic(2, 2, 0)
    assert out == float('inf')
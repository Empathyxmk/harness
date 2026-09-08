def dummy_resonance(a, b, c):
    return a * b * c

def test_rr_resonance():
    assert dummy_resonance(1, 2, 3) == 6

def test_rr_neg():
    assert dummy_resonance(-1, 2, 3) == -6
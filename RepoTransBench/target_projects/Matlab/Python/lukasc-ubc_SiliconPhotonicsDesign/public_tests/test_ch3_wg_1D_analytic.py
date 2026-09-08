def dummy_mul_public(a, b):
    return a * b

def test_scalar_input_public():
    y = dummy_mul_public(4, 3)
    assert y == 12

def test_zero_multiplier_public():
    y = dummy_mul_public(42, 0)
    assert y == 0
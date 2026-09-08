def dummy_resonator_calc_public(x):
    return x ** 2

def test_output_public():
    y = dummy_resonator_calc_public(6)
    assert y == 36

def test_negative_input_public():
    y = dummy_resonator_calc_public(-2)
    assert y == 4
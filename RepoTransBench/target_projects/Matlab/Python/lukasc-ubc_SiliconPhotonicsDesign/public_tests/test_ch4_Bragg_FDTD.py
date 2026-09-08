def dummy_bragg_val_public(a, b):
    return a + b

def test_bragg_value_public():
    val = dummy_bragg_val_public(22, -2)
    assert val == 20

def test_bragg_string_public():
    val = dummy_bragg_val_public(0, 5)
    assert val == 5
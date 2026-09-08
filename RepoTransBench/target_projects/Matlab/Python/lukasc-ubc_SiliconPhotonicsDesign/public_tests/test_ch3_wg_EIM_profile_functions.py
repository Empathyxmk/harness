def dummy_add_public(a, b):
    return a + b

def test_addition_public():
    result = dummy_add_public(10, 4)
    assert result == 14

def test_zero_public():
    result = dummy_add_public(99, -99)
    assert result == 0
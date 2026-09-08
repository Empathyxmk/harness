def dummy_func1_public(a, b):
    return a + b

def test_func1_public():
    y = dummy_func1_public(2, 5)
    assert y == 7

def test_func2_public():
    y = dummy_func1_public(-7, 3)
    assert y == -4
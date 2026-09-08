def g(x, y):
    return x * y

def g_alt(x, y):
    # Avoid division by zero
    return x // y if y else x

def test_g_and_g_alt():
    assert g(6, 5) == 30
    assert g_alt(20, 4) == 5
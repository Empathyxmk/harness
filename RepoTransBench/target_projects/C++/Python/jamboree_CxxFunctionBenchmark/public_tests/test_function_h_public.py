def add(a, b):
    return a + b

def test_public_basic_call():
    # Use different input/output than private test
    result = add(7, 8)
    assert result == 15

# More/different tests can be added as needed
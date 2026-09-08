def multiply(a, b):
    return a * b

def test_basic_rigtorp_multiply():
    # Just a smoke test for 'header presence' equivalent
    result = multiply(4, 6)
    assert result == 24
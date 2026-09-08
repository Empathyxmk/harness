from sample.core import add

def test_add_positive_numbers_public():
    # Different positive numbers than private test
    assert add(10, 5) == 15

def test_add_negative_and_positive_public():
    assert add(-6, 4) == -2

def test_add_zero_public():
    assert add(0, 19) == 19
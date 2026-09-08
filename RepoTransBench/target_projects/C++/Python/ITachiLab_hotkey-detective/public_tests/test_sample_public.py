def add(a, b):
    return a + b

def test_addition_works_public_sample():
    assert add(8, 4) == 12
    assert add(-1, 1) == 0
    assert add(100, 123) == 223
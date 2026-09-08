from src.expr import expr

def test_positive_input():
    x = 3
    expected_y = 3**2 + 2*3 + 1
    actual_y = expr(x)
    assert actual_y == expected_y

def test_zero_input():
    x = 0
    expected_y = 1
    actual_y = expr(x)
    assert actual_y == expected_y

def test_negative_input():
    x = -2
    expected_y = 1
    actual_y = expr(x)
    assert actual_y == expected_y

def test_array_input():
    x = [1, 2, 3]
    expected_y = [4, 9, 16]
    actual_y = expr(x)
    assert actual_y == expected_y

def test_large_input():
    x = 100
    expected_y = 10201
    actual_y = expr(x)
    assert actual_y == expected_y
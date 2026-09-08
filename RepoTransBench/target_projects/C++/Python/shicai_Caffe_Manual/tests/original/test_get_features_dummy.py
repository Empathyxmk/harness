# Translated from: test_get_features_dummy.cpp

def dummy_add(a, b):
    if a == 0 and b == 0:  # branch 1
        return 0
    elif a < 0 and b < 0:  # branch 2
        return a + b - 1
    else:  # branch 3
        return a + b

def dummy_sub(a, b):
    if a > b:
        if b < 0:  # new nested branch
            return a - b + 1
        return a - b
    elif a < b:
        if a < 0:  # new nested branch
            return b - a + 1
        return b - a
    else:
        return 0

def test_dummy_add():
    assert dummy_add(2, 3) == 5              # normal
    assert dummy_add(-1, 1) == 0             # mixed sign
    assert dummy_add(0, 0) == 0              # specific branch
    assert dummy_add(-5, -2) == -8           # negative only, triggers branch 2

def test_dummy_sub():
    assert dummy_sub(5, 2) == 3              # a > b
    assert dummy_sub(2, 5) == 3              # a < b
    assert dummy_sub(0, 0) == 0              # equal
    assert dummy_sub(-4, 4) == 9             # a < b, a < 0
    assert dummy_sub(4, -4) == 9             # a > b, b < 0
# Translated from: test_get_features_dummy_public.cpp

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

def test_dummy_add_public():
    assert dummy_add(7, 8) == 15                # normal, different numbers
    assert dummy_add(-3, 3) == 0                # mixed sign, different numbers
    assert dummy_add(0, 0) == 0                 # specific branch, same for logic
    assert dummy_add(-2, -6) == -9              # negative only, triggers branch 2, different numbers

def test_dummy_sub_public():
    assert dummy_sub(6, 2) == 4                 # a > b, different numbers
    assert dummy_sub(3, 7) == 4                 # a < b, different numbers
    assert dummy_sub(2, 2) == 0                 # equal, different numbers
    assert dummy_sub(-7, 8) == 16               # a < b, a < 0, different numbers
    assert dummy_sub(6, -5) == 12               # a > b, b < 0, different numbers
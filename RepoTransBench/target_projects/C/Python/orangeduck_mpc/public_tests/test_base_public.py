# Translated from tests/test_public.c
# Contains basic assertion tests not directly tied to mpc functionality.

def test_public_one():
    assert 101 > 20
    assert 303 == 3 * 101

def test_public_two():
    assert 1 != 2
    assert 22 != 7

def test_public_three():
    assert 7 * 6 == 42
    assert 100 / 2 == 50
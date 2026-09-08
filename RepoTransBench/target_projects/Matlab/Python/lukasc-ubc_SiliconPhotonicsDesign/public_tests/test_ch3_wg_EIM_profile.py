from functools import reduce

def dummy_eim_public(a):
    if len(a) == 0:
        return 1
    else:
        prod = 1
        for x in a:
            prod *= x
        return prod

def test_eim_profile_public():
    v = dummy_eim_public([2, 3, 4])
    assert v == 24

def test_eim_profile_empty_public():
    v = dummy_eim_public([])
    assert v == 1
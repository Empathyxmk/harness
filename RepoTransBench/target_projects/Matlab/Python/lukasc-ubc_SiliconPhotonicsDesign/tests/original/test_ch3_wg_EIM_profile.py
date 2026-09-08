def dummy_eim2(a, b):
    if a == 0:
        return 0
    else:
        return a / b

def test_basic():
    eim = dummy_eim2(4, 2)
    assert eim == 2

def test_zero():
    eim = dummy_eim2(0, 4)
    assert eim == 0
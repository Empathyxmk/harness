from pyope.ope import ValueRange

def test_range_size_public():
    r = ValueRange(-10, 20)
    assert r.size() == 31

def test_range_copy_public():
    r1 = ValueRange(100, 200)
    r2 = r1.copy()
    assert r1.start == r2.start and r1.end == r2.end and r1 is not r2

def test_range_contains_public():
    r = ValueRange(15, 25)
    assert r.contains(20) is True
    assert r.contains(14) is False
    assert r.contains(25) is True
    assert r.contains(26) is False

def test_range_repr_public():
    r = ValueRange(5, 10)
    assert "ValueRange" in repr(r)
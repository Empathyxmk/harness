import pytest

# Translation of test_visit_struct_boost_fusion.cpp
# Note: this test is conceptual because Python has no Boost Fusion.
# We'll simulate the struct visitation pattern.

class TestStructOne:
    def __init__(self, a=0, b=0.0, c=""):
        self.a = a
        self.b = b
        self.c = c

class TestStructTwo:
    def __init__(self, d=0.0, i=0, b=False):
        self.d = d
        self.i = i
        self.b = b

def test_struct_one_fields():
    s = TestStructOne(5, 7.5, "asdf")
    assert s.a == 5
    assert s.b == 7.5
    assert s.c == "asdf"
    assert list(vars(s).keys()) == ["a", "b", "c"]

def test_struct_two_fields():
    s = TestStructTwo(-1.0, 5, False)
    assert s.d == -1.0
    assert s.i == 5
    assert s.b == False
    assert list(vars(s).keys()) == ["d", "i", "b"]

def test_struct_cmp():
    def struct_cmp(t1, t2):
        for field in ["d", "i", "b"]:
            v1 = getattr(t1, field)
            v2 = getattr(t2, field)
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0

    f1 = TestStructTwo(1.5, 1, True)
    f2 = TestStructTwo(10.0, 2, True)
    assert struct_cmp(f1, f1) == 0
    assert struct_cmp(f1, f2) == -1
    f1.d = 10
    assert struct_cmp(f1, f2) == -1
    f1.i = 3
    assert struct_cmp(f1, f2) == 1
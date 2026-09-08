import pytest

# Translation of test_visit_struct_intrusive.cpp

class Foo:
    def __init__(self, b=True, i=0, f=0.0):
        self.b = b
        self.i = i
        self.f = f

def test_foo_fields_and_names():
    s = Foo(True, 5, 7.5)
    assert s.b == True
    assert s.i == 5
    assert s.f == 7.5
    assert list(vars(s).keys()) == ["b", "i", "f"]

def test_visitor_collect_names_values():
    s = Foo(True, 5, 7.5)
    names = []
    values = []
    for field in ["b", "i", "f"]:
        names.append(field)
        values.append(getattr(s, field))
    assert names == ["b", "i", "f"]
    assert values == [True, 5, 7.5]
    # Change and check
    s.b = False
    s.i = 19
    s.f = -1.5
    new_names = []
    new_values = []
    for field in ["b", "i", "f"]:
        new_names.append(field)
        new_values.append(getattr(s, field))
    assert new_names == ["b", "i", "f"]
    assert new_values == [False, 19, -1.5]

def test_struct_cmp_intrusive():
    # Simulate lex_compare_visitor order semantics
    def struct_cmp(t1, t2):
        for field in ["b", "i", "f"]:
            v1 = getattr(t1, field)
            v2 = getattr(t2, field)
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0

    f1 = Foo(True, 1, 1.5)
    f2 = Foo(True, 2, 10.0)
    assert struct_cmp(f1, f1) == 0
    assert struct_cmp(f1, f2) == -1
    assert struct_cmp(f2, f2) == 0
    assert struct_cmp(f2, f1) == 1
    f1.i = 3
    assert struct_cmp(f1, f2) == 1
    f1.i = 2
    assert struct_cmp(f1, f2) == -1
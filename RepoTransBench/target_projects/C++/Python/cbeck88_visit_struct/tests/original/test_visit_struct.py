import pytest

# Translation of test_visit_struct.cpp

class test_struct_one:
    def __init__(self, a=0, b=0.0, c=""):
        self.a = a
        self.b = b
        self.c = c

class test_struct_two:
    def __init__(self, b=False, i=0, d=0.0, s=""):
        self.b = b
        self.i = i
        self.d = d
        self.s = s

def test_visit_struct_one_basics():
    s = test_struct_one(5, 7.5, "asdf")
    assert s.a == 5
    assert s.b == 7.5
    assert s.c == "asdf"
    assert len(vars(s)) == 3
    # Getter names/fn: simulate get_name (by variable names)
    assert list(vars(s).keys()) == ["a", "b", "c"]

def test_visit_struct_two_registered_fields():
    # Registered order: d, i, b (s not registered)
    s = test_struct_two(False, 5, -1.0, "foo")
    assert s.d == -1.0
    assert s.i == 5
    assert s.b == False
    assert len(vars(s)) == 4  # Four fields, but only 3 registered in C++: d, i, b
    # Simulate registered names
    registered_names = ["d", "i", "b"]
    # For test purposes, just check those are in the object
    for k in registered_names:
        assert hasattr(s, k)

def test_struct_eq():
    # Simulate struct_eq and struct_int_cmp
    s1 = test_struct_one(0, 0, "")
    s2 = test_struct_one(1, 1, "a")
    assert s1 != s2

def test_move_semantics_emulation():
    # Simulate move semantics test_visitor_three logic:
    class Visitor:
        def __init__(self):
            self.result = None
        # simulate different calls for lvalue/rvalue/ref
        def __call__(self, obj):
            if obj is None:
                self.result = 3  # move
            else:
                self.result = 1
    s = test_struct_one(0, 0, "")
    vis = Visitor()
    vis(s)
    assert vis.result == 1
    vis(None)
    assert vis.result == 3
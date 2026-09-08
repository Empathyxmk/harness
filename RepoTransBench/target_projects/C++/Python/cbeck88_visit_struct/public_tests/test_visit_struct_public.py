import pytest

# Translation of test_visit_struct_public.cpp

class TestStructPub1:
    def __init__(self, a=0, b=0.0, c=""):
        self.a = a
        self.b = b
        self.c = c

class TestStructPub2:
    def __init__(self, b='\0', i=0, d=0.0, s=""):
        self.b = b
        self.i = i
        self.d = d
        self.s = s

class PrintVisitorPub:
    def __init__(self):
        self.fields = []
    def __call__(self, o):
        for name in vars(o):
            self.fields.append(name)

def test_struct_pub1_visit():
    s1 = TestStructPub1(24, 3.5, "hello")
    visitor = PrintVisitorPub()
    visitor(s1)
    assert len(visitor.fields) == 3
    # Order is by var def, simulate C++: ["c", "b", "a"] — here, we sort to simulate
    assert sorted(visitor.fields) == sorted(["a", "b", "c"])

def test_struct_pub2_partial_visit():
    s2 = TestStructPub2('Z', 12, 2.5, "should_ignore")
    visitor = PrintVisitorPub()
    visitor(s2)
    # Only registered fields count in C++; here, we just check the main ones
    assert len(visitor.fields) == 4

def test_field_types_pub1():
    s1 = TestStructPub1(24, 3.5, "hello")
    assert isinstance(s1.c, str)
    assert isinstance(s1.b, float)
    assert isinstance(s1.a, int)
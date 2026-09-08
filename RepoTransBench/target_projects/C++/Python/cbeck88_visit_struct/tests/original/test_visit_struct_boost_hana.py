import pytest

# Translation of test_visit_struct_boost_hana.cpp
# Python has no Hana equivalent, simulate field registration and types

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

class TestStructThree:
    def __init__(self, i1=0, i2=0):
        self.i1 = i1
        self.i2 = i2

def test_struct_one_fields_types():
    s = TestStructOne(5, 7.5, "asdf")
    assert isinstance(s.a, int)
    assert isinstance(s.b, float)
    assert isinstance(s.c, str)
    assert list(vars(s).keys()) == ["a", "b", "c"]

def test_struct_two_fields_types():
    s = TestStructTwo(-1.0, 5, False)
    assert isinstance(s.d, float)
    assert isinstance(s.i, int)
    assert isinstance(s.b, bool)
    assert list(vars(s).keys()) == ["d", "i", "b"]

def test_struct_cmp_hana():
    def struct_cmp(t1, t2, fields):
        for field in fields:
            v1 = getattr(t1, field)
            v2 = getattr(t2, field)
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0

    f1 = TestStructOne(10, 7.5, "a")
    f2 = TestStructOne(11, 7.5, "b")
    assert struct_cmp(f1, f1, ["a", "b", "c"]) == 0
    assert struct_cmp(f1, f2, ["a", "b", "c"]) == -1
    f1.a = 13
    assert struct_cmp(f1, f2, ["a", "b", "c"]) == 1
    f1.a = 11
    assert struct_cmp(f1, f2, ["a", "b", "c"]) == -1

def test_types_visitor():
    # Emulate C++ logic: list out types of fields in registration order
    fields_types_one = [("a", int), ("b", float), ("c", str)]
    types_strings = []
    for _, t in fields_types_one:
        if t is int:
            types_strings.append("int")
        elif t is float:
            types_strings.append("float")
        elif t is str:
            types_strings.append("std::string")
    assert types_strings == ["int", "float", "std::string"]
    fields_types_two = [("d", float), ("i", int), ("b", bool)]
    types_strings2 = []
    for _, t in fields_types_two:
        if t is float:
            types_strings2.append("double")
        elif t is int:
            types_strings2.append("int")
        elif t is bool:
            types_strings2.append("bool")
    assert types_strings2 == ["double", "int", "bool"]
    fields_types_three = [("i1", int), ("i2", int)]
    types_strings3 = []
    for _, t in fields_types_three:
        if t is int:
            types_strings3.append("int")
    assert types_strings3 == ["int", "int"]
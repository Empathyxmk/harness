import pytest
import math
import sys
import array
import numbers
import copy
import cmath

def almost_equal(a, b, tol=1e-9):
    return abs(a - b) < tol

def test_fundamental_scalar():
    # We'll test a representative set of types, as per C++ code
    fundamentals = [
        (int, 2),
        (float, 2.0),
        (bool, True),
        (str, 'a')
    ]
    for typ, value in fundamentals:
        val = typ(value)
        arr = [val]
        assert arr[0] == val
        arr[0] = value
        assert arr[0] == value

def test_all_fundamental_scalar():
    # int8, uint8, int16, ... analogous types
    # Python doesn't have these exact types, but test with int, float, bool, str
    for typ, value in [
        (int, 42),
        (float, 3.14),
        (bool, False),
        (str, "abc"),
    ]:
        val = typ(value)
        arr = [val]
        assert arr[0] == val
        arr[0] = value
        assert arr[0] == value

def test_fundamental_vector():
    for typ, val in [(int, 0), (float, 0.0)]:
        N = 10
        arr = [typ(i) for i in range(N)]
        assert len(arr) == N
        for i, v in enumerate(arr):
            assert v == i

def test_all_fundamental_vector():
    for typ in (int, float, bool, str):
        N = 10
        arr = [typ(i % 2 if typ is bool else i) for i in range(N)]
        assert len(arr) == N
        for i in range(N):
            assert isinstance(arr[i], typ)

def test_complex():
    for S in [float, complex]:
        v1 = complex(+1.1, -3.4)
        v2 = complex(0.0, 0.0)
        v3 = complex(+2.2, -5.6)
        arr = [v1]
        assert arr[0] == v1
        arr[0] = v3
        assert arr[0] == v3
        # Vector of complex
        b = [complex(1.1, 2.2), complex(3.3, 4.4)]
        a = list(b)
        assert a == b
        # "magnitude" in C++ - sqrt(a.real^2 + a.imag^2)
        magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in b]
        assert len(magnitude) == len(b)
        for i in range(len(magnitude)):
            ref = abs(b[i])
            assert almost_equal(magnitude[i], ref)

def test_all_complex():
    test_complex()

def test_mxarray_memory():
    # Python references/assignment semantics
    one = [1.0]
    assert one[0] == 1.0
    moved_one = one
    assert moved_one[0] == 1.0
    empty = []
    moved_one, empty = empty, moved_one
    assert moved_one == []
    assert empty == [1.0]

def test_mxarray_string():
    value = "string value."
    value2 = "another string."
    str_vector = ["element1", "element2", "element3"]
    str_vector_vector = [str_vector, str_vector]
    nested_string = [str_vector_vector, str_vector_vector]
    value3 = list(str_vector)
    value4 = copy.deepcopy(nested_string)
    assert isinstance(value, str)
    assert isinstance(value2, str)
    assert isinstance(value3, list)
    assert isinstance(value4, list)
    assert value == "string value."
    assert value2 == "another string."
    assert value3 == str_vector
    assert len(value4) == 2
    # Mutate
    value = 'S' + value[1:]
    assert value == "String value."
    value3[0] = "Element1"
    assert value3[0] == "Element1"
    value4[0] = nested_string[0]

def test_mxarray_cell():
    cell_array = [None, None]
    assert cell_array[0] is None
    assert cell_array[1] is None
    cell_array[0] = 10.1
    cell_array[1] = "text."
    assert cell_array[0] == 10.1
    assert cell_array[1] == "text."
    cell_array = [None, None]
    assert cell_array[0] is None
    assert cell_array[1] is None

def test_mxarray_struct():
    struct_array = {}
    struct_array["field1"] = None
    struct_array["field2"] = None
    struct_array["field3"] = None
    assert struct_array["field1"] is None
    struct_array["field1"] = 10.1
    struct_array["field2"] = "text."
    struct_array["field3"] = [2.0] * 10
    struct_array["field4"] = "additional value."
    assert struct_array["field1"] == 10.1
    assert struct_array["field2"] == "text."
    vector_of_2 = struct_array["field3"]
    assert struct_array["field4"] == "additional value."
    assert len(vector_of_2) == 10
    for val in vector_of_2:
        assert val == 2.0
    struct_array = {k: None for k in ["field1", "field2", "field3"]}
    assert struct_array["field1"] is None

class MyCellObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MyStructObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def mxarray_from_mycellobject(obj):
    return [obj.name, obj.value]

def mxarray_to_mycellobject(arr):
    o = MyCellObject(arr[0], arr[1])
    return o

def mxarray_from_mystructobject(obj):
    return {"name": obj.name, "value": obj.value}

def mxarray_to_mystructobject(d):
    return MyStructObject(d["name"], d["value"])

def test_custom_cell():
    object = MyCellObject("foo", [1.0]*10)
    array = mxarray_from_mycellobject(object)
    assert array[0] == "foo"
    assert isinstance(array[1], list) and len(array[1]) == 10
    object2 = mxarray_to_mycellobject(array)
    assert object.name == object2.name
    assert len(object.value) == len(object2.value)

def test_custom_struct():
    object = MyStructObject("foo", [1.0]*10)
    array = mxarray_from_mystructobject(object)
    assert array["name"] == "foo"
    assert isinstance(array["value"], list) and len(array["value"]) == 10
    object2 = mxarray_to_mystructobject(array)
    assert object.name == object2.name
    assert len(object.value) == len(object2.value)
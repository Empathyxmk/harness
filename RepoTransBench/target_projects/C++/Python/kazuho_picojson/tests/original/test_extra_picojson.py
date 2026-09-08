import pytest
import math
from src.picojson import value, null

def test_null_type():
    n = value()
    assert n.is_null()
    assert n.serialize() == "null"

def test_type_accessors():
    b = value(True)
    assert b.is_bool()
    assert b.get(bool) == True

    d = value(3.14)
    assert d.is_double()
    assert d.get(float) == 3.14

    s = value("foo")
    assert s.is_string()
    assert s.get(str) == "foo"

    arr = value.array()
    arr.append(value(7.0))
    a = value(arr)
    assert a.is_array()
    assert len(a.get(type(value.array))) == 1

    obj = value.object()
    obj["bar"] = value(42.0)
    o = value(obj)
    assert o.is_object()
    assert o.get(type(value.object))["bar"].get(float) == 42.0

def test_operators_and_comparisons():
    v1 = value(1.0)
    v2 = value(1.0)
    v3 = value(2.0)
    assert v1 == v2
    assert not (v1 != v2)
    assert v1 != v3

    o1 = value.object()
    o2 = value.object()
    o1["a"] = value(True)
    o2["a"] = value(True)
    obj1, obj2 = value(o1), value(o2)
    assert obj1 == obj2

    o2["b"] = value(False)
    obj3 = value(o2)
    assert obj1 != obj3

def test_serialization_and_parsing_errors():
    obj = value.object()
    obj["foo"] = value("\"quoted\"")
    v1 = value(obj)

    ser = v1.serialize()
    from src.picojson import parse
    parse_target = value()
    err = []
    parse(parse_target, ser, ser, err)
    assert err == [] or err == ""
    assert parse_target.is_object()

    malformed = ["{[}", "{", "{\"a\":", "tru", "\"\\uZZZZ\""]
    for s in malformed:
        v2 = value()
        err2 = []
        parse(v2, s, s, err2)
        assert err2 or not (err2 == [])

def test_array_and_object_modifiers():
    arr = value.array()
    arr.append(value(10.0))
    arr_v = value(arr)
    assert arr_v.is_array()
    assert arr_v.get(type(value.array))[0].get(float) == 10.0

    obj = value.object()
    obj["x"] = value(99.9)
    obj_v = value(obj)
    assert obj_v.get(type(value.object))["x"].get(float) == 99.9

    oref = obj_v.get(type(value.object))
    oref.pop("x")
    assert oref.count("x") == 0

    oref[""] = value(False)
    assert oref.count("") == 1
    oref.pop("")
    assert oref.count("") == 0

def test_number_edge_cases():
    # NaN and infinity rejected
    import math
    with pytest.raises(OverflowError):
        value(math.nan)
    with pytest.raises(OverflowError):
        value(math.inf)

def test_bad_get():
    v = value(42.0)
    with pytest.raises(Exception):
        v.get(str)

def test_prettify():
    o = value.object()
    o["x"] = value(True)
    o["y"] = value(3.14)
    v = value(o)
    pretty = v.serialize(pretty=True)
    assert '\n' in pretty or '\t' in pretty

def test_copy_swap():
    v1, v2 = value(42.0), value(True)
    tmp = value(v1)
    v1.swap(v2)
    assert v1.is_bool() and v2.is_double()
    v1.swap(v2)
    assert v1.is_double() and v2.is_bool()
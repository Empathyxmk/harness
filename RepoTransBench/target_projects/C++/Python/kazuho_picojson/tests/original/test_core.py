import pytest
import math
from src.picojson import value, null

def test_value_constructors():
    # TEST( (true),  "true");
    assert value(True).serialize() == "true"
    assert value(False).serialize() == "false"
    assert value(42.0).serialize() == "42"
    assert value("hello").serialize() == '"hello"'
    assert value("hello").serialize() == '"hello"'
    # TEST( ("hello", 4), "\"hell\"");  # Not directly translatable to Python, as str cannot have N
    # So use slicing for demonstration
    assert value("hello"[:4]).serialize() == '"hell"'

def test_double_roundtrip():
    a = 1.0
    for i in range(1024):
        vi = value(a)
        from io import StringIO
        s = StringIO()
        s.write(vi.serialize())
        s.seek(0)
        ser = s.read()
        v2 = value(float(ser))
        b = v2.get(float)
        if i < 53:
            assert a == b
        else:
            assert abs(a-b)/b <= 1e-8
        a *= 2

def test_simple_json_parsing():
    # "false" as bool
    v = value()
    err = []
    s = "false"
    from src.picojson import parse
    parse(v, s, s, err)
    assert err == [] or err == ""
    assert v.is_bool()
    assert v.get(bool) == False

    # "true" as bool
    v = value()
    err = []
    s = "true"
    parse(v, s, s, err)
    assert err == [] or err == ""
    assert v.is_bool()
    assert v.get(bool) == True

    # "90.5" as double
    v = value()
    err = []
    s = "90.5"
    parse(v, s, s, err)
    assert v.is_double()
    assert math.isclose(v.get(float), 90.5)

    # "1.7976931348623157e+308" as DBL_MAX
    v = value()
    err = []
    s = "1.7976931348623157e+308"
    parse(v, s, s, err)
    assert v.is_double()
    # float as DBL_MAX
    assert math.isclose(v.get(float), 1.7976931348623157e+308)

    # string test
    v = value()
    s = '"hello"'
    parse(v, s, s, err)
    assert v.is_string()
    assert v.get(str) == "hello"

    # string with escapes
    v = value()
    s = "\"\\\"\\\\\\/\\b\\f\\n\\r\\t\""
    parse(v, s, s, err)
    assert v.is_string()
    # Result string will have escape chars, check basic value
    # Must decode via JSON
    import json
    assert json.loads(s) == v.get(str)

def test_empty_array_and_object():
    # TEST(array, "[]");
    v = value()
    from src.picojson import parse
    s = "[]"
    err = []
    parse(v, s, s, err)
    assert v.is_array()
    assert len(v.get(type(v.array))) == 0

    # TEST(object, "{}");
    v = value()
    s = "{}"
    parse(v, s, s, err)
    assert v.is_object()
    assert len(v.get(type(v.object))) == 0

def test_array_type_access():
    v = value()
    s = "[1,true,\"hello\"]"
    from src.picojson import parse
    err = []
    parse(v, s, s, err)
    assert v.is_array()
    arr = v.get(type(v.array))
    assert len(arr) == 3
    assert v.contains(0)
    assert arr[0].is_double()
    assert arr[0].get(float) == 1.0
    assert v.contains(1)
    assert arr[1].is_bool()
    assert arr[1].get(bool) == True
    assert v.contains(2)
    assert arr[2].is_string()
    assert arr[2].get(str) == "hello"
    assert not v.contains(3)

def test_object_type_access():
    v = value()
    s = '{"a": true}'
    from src.picojson import parse
    err = []
    parse(v, s, s, err)
    assert v.is_object()
    obj = v.get(type(v.object))
    assert len(obj) == 1
    assert v.contains("a")
    assert obj["a"].is_bool()
    assert obj["a"].get(bool) == True
    # check default serialization
    assert v.serialize() == '{"a":true}'
    assert not v.contains("z")

def test_object_and_array_modification():
    v1 = value()
    v1.set(type(value.object), value.object())
    v1.get(type(value.object))["114"] = value("514")
    v1.get(type(value.object))["364"] = value()
    v1.get(type(value.object))["364"].set(type(value.array), value.array())
    v1.get(type(value.object))["364"].get(type(value.array)).append(value(334.0))
    v2 = v1.get(type(value.object))["1919"] = value()
    v1.get(type(value.object))["1919"].set(type(value.object), value.object())
    v1.get(type(value.object))["1919"].get(type(value.object))["893"] = value(810.0)
    assert v1.serialize() == '{"114":"514","1919":{"893":810},"364":[334]}'

def test_json_syntax_errors():
    from src.picojson import parse
    v = value()
    # TEST("falsoa", "1 near: oa");
    err = []
    parse(v, "falsoa", "falsoa", err)
    assert err or not (err == [])

    # TEST("{]", "1 near: ]");
    err = []
    parse(v, "{]", "{]", err)
    assert err or not (err == [])

    # TEST("\n\bbell", "2 near: bell");
    err = []
    parse(v, "\n\bbell", "\n\bbell", err)
    assert err or not (err == [])

    # TEST("\"abc\nd\"", "1 near: ");
    err = []
    parse(v, "\"abc\nd\"", "\"abc\nd\"", err)
    assert err or not (err == [])

def test_deep_compare_equality():
    from src.picojson import parse
    v1, v2 = value(), value()
    s1 = '{"b": true, "a": [1,2,"three"], "d": 2}'
    s2 = '{"d": 2.0, "b": true, "a": [1,2,"three"]}'
    parse(v1, s1, s1)
    parse(v2, s2, s2)
    assert v1 == v2

    s3 = '{"d": 2.0, "a": [1,"three"], "b": true}'
    parse(v2, s3, s3)
    assert v1 != v2

    s4 = '{"d": 2.0, "a": [1,2,"three"], "b": false}'
    parse(v2, s4, s4)
    assert v1 != v2

def test_erase_and_remove():
    v1 = value()
    s = '{"b": true, "a": [1,2,"three"], "d": 2}'
    from src.picojson import parse
    parse(v1, s, s)
    o = v1.get(type(value.object))
    del o["b"]
    a = o["a"].get(type(value.array))
    # Remove 'three' from the array
    for i, elem in enumerate(a):
        if elem.is_string() and elem.get(str) == "three":
            a.pop(i)
            break
    v2 = value()
    s2 = '{"a": [1,2], "d": 2}'
    parse(v2, s2, s2)
    assert v1 == v2

def test_integral_number_serialization():
    assert value(3.0).serialize() == "3"

def test_swap():
    v1 = value(True)
    v2 = value()
    v1.swap(v2)
    assert v1.is_null()
    assert v2.get(bool) == True

    v1 = value("a")
    v2 = value(1.0)
    v1.swap(v2)
    assert v1.get(float) == 1.0
    assert v2.get(str) == "a"

    v1 = value(value.object())
    v2 = value(value.array())
    v1.swap(v2)
    assert v1.is_array()
    assert v2.is_object()

def test_prettify_and_nonprettify():
    v = value()
    s = '{"a": 1, "b": [2, {"b1": "abc"}], "c": {}, "d": []}'
    from src.picojson import parse
    parse(v, s, s)
    default_serial = v.serialize()
    assert default_serial == '{"a":1,"b":[2,{"b1":"abc"}],"c":{},"d":[]}'
    pretty_serial = v.serialize(pretty=True)
    assert '\n' in pretty_serial or '\t' in pretty_serial

def test_nan_infinity_not_allowed():
    import math
    with pytest.raises(OverflowError):
        value(math.nan)
    with pytest.raises(OverflowError):
        value(math.inf)

def test_wrong_type_access():
    v = value(123.)
    assert not v.is_bool()
    with pytest.raises(Exception):
        v.get(bool)

def test_array_object_evaluate_as_boolean():
    # Double 0 is false
    v1 = value(0.0)
    assert not v1.evaluate_as_boolean()

    v2 = value(1.0)
    assert v2.evaluate_as_boolean()

def test_simple_api():
    from src.picojson import parse
    v = value()
    err = parse(v, "[ 1, \"abc\" ]", "[ 1, \"abc\" ]")
    assert v.is_array()
    arr = v.get(type(value.array))
    assert len(arr) == 2
    assert arr[0].is_double()
    assert arr[0].get(float) == 1
    assert arr[1].is_string()
    assert arr[1].get(str) == "abc"
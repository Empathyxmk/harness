import pytest
import math
from src.picojson import value, null, parse

def test_public_value_constructors():
    # "false", "true", "13.7", "world", "public", "different"
    assert value(False).serialize() == "false"
    assert value(True).serialize() == "true"
    assert value(13.7).serialize() == "13.7"
    assert value("world").serialize() == '"world"'
    # ("public", 6) == slice up to 6
    assert value("public"[:6]).serialize() == '"public"'
    assert value("different").serialize() == '"different"'

def test_public_double_roundtrip():
    a = 3.5
    for i in range(100):
        vi = value(a)
        import io
        s = io.StringIO()
        s.write(vi.serialize())
        s.seek(0)
        ser = s.read()
        vo = value(float(ser))
        b = vo.get(float)
        if i < 53:
            assert a == b
        else:
            assert abs(a - b) / (b if b != 0 else 1) <= 1e-8
        a *= 1.8

def test_numeric_parsing():
    v = value()
    in_ = "123.456"
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_double()
    assert math.isclose(v.get(float), 123.456)
    assert v.serialize() == "123.456"

def test_string_parsing():
    v = value()
    in_ = '"testing"'
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_string()
    assert v.get(str) == "testing"
    assert v.serialize() == '"testing"'

def test_array_parsing():
    v = value()
    in_ = "[1,2,3]"
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_array()
    arr = v.get(type(value.array))
    assert len(arr) == 3
    assert v.serialize() == "[1,2,3]"

def test_object_parsing():
    v = value()
    in_ = '{"alpha":100,"beta":false}'
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_object()
    obj = v.get(type(value.object))
    assert len(obj) == 2
    assert v.serialize() == '{"alpha":100,"beta":false}'

def test_null_parsing():
    v = value()
    in_ = "null"
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_null()
    assert v.serialize() == "null"

def test_public_bool_array():
    v = value()
    in_ = "[false,true,false]"
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_array()
    arr = v.get(type(value.array))
    assert len(arr) == 3
    assert v.serialize() == "[false,true,false]"
    assert arr[0].get(bool) == False
    assert arr[1].get(bool) == True
    assert arr[2].get(bool) == False

def test_public_number_edge_case():
    v = value()
    in_ = "-0.987654321"
    err = []
    parse(v, in_, in_, err)
    assert err == [] or err == ""
    assert v.is_double()
    assert math.isclose(v.get(float), -0.987654321)
    assert v.serialize() == "-0.987654321"
import pytest
import sys
from src.json11 import Json

def test_parse_max_depth():
    deep = "["
    for i in range(201):
        deep += "["
    for i in range(201):
        deep += "]"
    err = []
    res = Json.parse(deep, err)
    assert res.is_null()
    assert err

def test_parse_invalid_json():
    err = []
    j1 = Json.parse("{ missing colon }", err)
    assert j1.is_null()
    assert err

    err = []
    j2 = Json.parse("\"bad \\u00XZ sequence\"", err)
    assert j2.is_null()
    assert err

    err = []
    j3 = Json.parse("[1, 2,]", err)
    assert j3.is_null()
    assert err

    err = []
    # Control character in string (0x01)
    bad = "\"\x01\""
    j4 = Json.parse(bad, err)
    assert j4.is_null()
    assert err

    err = []
    j5 = Json.parse("\"ok\" foo", err)
    assert j5.is_null()
    assert err

def test_equality_comparisons():
    jnull = Json(None)
    jnull2 = Json()
    assert jnull == jnull2

    jbool = Json(True)
    jbool2 = Json(False)
    assert jbool != jbool2

    jint = Json(7)
    jint2 = Json(7.0)
    assert jint == jint2
    assert not(jint < jint2)
    assert not(jint2 < jint)

    jstr = Json("abc")
    jstr2 = Json("abd")
    assert jstr < jstr2

    arr1 = Json.array([1, 2])
    arr2 = Json.array([2, 1])
    assert arr1 != arr2

def test_accessors_extras():
    arr = Json.array([1, 2])
    assert arr[0] == Json(1)
    assert arr[100].is_null()

    obj = Json.object({"x": 9})
    assert obj["x"] == Json(9)
    assert obj["notfound"].is_null()

    i = Json(123)
    assert i.array_items() == []
    assert i.object_items() == {}
    assert i["fake"].is_null()
    assert i[0].is_null()

def test_json_dump_edge():
    jstr = Json("")
    assert jstr.dump().startswith('"')

    arr = Json.array([Json("foo"), Json()])
    d = arr.dump()
    assert "foo" in d

    obj = Json.object({"k": Json("v"), "n": Json()})
    d2 = obj.dump()
    assert "k" in d2 and "v" in d2

    j = Json.object({"q": Json("\b\t\n\r\"\\")})
    s = j.dump()
    assert "\\b" in s and "\\t" in s

    import sys
    jmin = Json(-sys.maxsize-1)
    jmax = Json(sys.float_info.max)
    sjmin = jmin.dump()
    sjmax = jmax.dump()
    assert sjmin and sjmax

def test_null_type_behavior():
    jnull = Json()
    jnull2 = jnull
    jnull2 = Json(None)
    assert jnull2.is_null()
    assert jnull == None
    jobj = Json.object({})
    assert not jobj.is_null()
    assert jobj.type() == Json.OBJECT
    jarr = Json.array([])
    assert jarr.type() == Json.ARRAY
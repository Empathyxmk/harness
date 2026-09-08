import pytest
from src.json11 import Json

def test_json11_public_advanced():
    array_test = '[100, "hello", 3.14, false, null, {"nested": [1, 2]}]'
    err = []
    json = Json.parse(array_test, err)
    assert json.is_array()
    assert json[0] == 100
    assert json[1] == "hello"
    assert json[2].number_value() == 3.14
    assert json[3] == False
    assert json[4].is_null()
    assert json[5].is_object()
    assert len(json[5]["nested"].array_items()) == 2
    assert json[5]["nested"][0] == 1
    assert json[5]["nested"][1] == 2

    object_test = '{"foo":42,"bar":[true,{"baz":0.5}]}'
    json = Json.parse(object_test, err)
    assert json["foo"] == 42
    assert json["bar"].is_array()
    assert json["bar"][0] == True
    assert json["bar"][1]["baz"].number_value() == 0.5

    esc_test = r'{"str":"abc\\def\"ghi\njkl\t"}'
    esc = Json.parse(esc_test, err)
    assert esc["str"].string_value() == "abc\\def\"ghi\njkl\t"

    bool_test = '[true,false,true]'
    json = Json.parse(bool_test, err)
    assert json[0] == True
    assert json[1] == False
    assert json[2] == True

    complex_obj = '{"a":[{"k":1.1},{},{"k":2.3}],"x":0,"b":{"y":true, "z":"qq"}}'
    json = Json.parse(complex_obj, err)
    assert len(json["a"].array_items()) == 3
    assert json["a"][0]["k"].number_value() == 1.1
    assert json["a"][2]["k"].number_value() == 2.3
    assert json["a"][1].is_object() and len(json["a"][1].object_items()) == 0
    assert json["x"] == 0
    assert json["b"]["y"] == True
    assert json["b"]["z"] == "qq"
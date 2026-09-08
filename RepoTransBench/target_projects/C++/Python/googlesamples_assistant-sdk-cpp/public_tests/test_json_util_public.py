import pytest
from src.assistant.json_util import JsonUtil

def test_parse_valid_simple_json_public():
    json_str = '{"hello": "public", "answer": 100}'
    doc = JsonUtil.Parse(json_str)
    assert doc.ok()

    obj = doc.ValueOrDie()
    assert obj["hello"] == "public"
    assert obj["answer"] == 100

def test_parse_invalid_json_public():
    json_str = '{"unterminated: 42'
    doc = JsonUtil.Parse(json_str)
    assert not doc.ok()

def test_json_stringify_object_public():
    obj = {"food": "pizza", "qty": 4}
    json_result = JsonUtil.Stringify(obj)
    assert "pizza" in json_result
    assert "qty" in json_result
    assert "4" in json_result

def test_parse_bool_and_array_public():
    json_str = '{"success": true, "nums": [10, 20, 30]}'
    doc = JsonUtil.Parse(json_str)
    assert doc.ok()
    obj = doc.ValueOrDie()
    assert obj["success"] is True
    assert obj["nums"][0] == 10
    assert obj["nums"][1] == 20
    assert obj["nums"][2] == 30
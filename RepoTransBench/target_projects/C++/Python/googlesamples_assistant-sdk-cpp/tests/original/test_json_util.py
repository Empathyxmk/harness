import pytest
from src.assistant.json_util import JsonUtil

def test_parse_valid_json():
    json_str = '{"key": "value", "num": 123}'
    doc = JsonUtil.Parse(json_str)
    assert doc.ok()

    obj = doc.ValueOrDie()
    assert obj["key"] == "value"
    assert obj["num"] == 123

def test_parse_invalid_json():
    json_str = "{ key: 123 "
    doc = JsonUtil.Parse(json_str)
    assert not doc.ok()

def test_stringify_object():
    obj = {"status": "ok", "id": 1}

    json_result = JsonUtil.Stringify(obj)
    assert "ok" in json_result
    assert "id" in json_result
    assert "1" in json_result

def test_parse_array_and_bool():
    json_str = '{"flag": false, "arr": [1,2,3]}'
    doc = JsonUtil.Parse(json_str)
    assert doc.ok()
    obj = doc.ValueOrDie()
    assert obj["flag"] is False
    assert obj["arr"][0] == 1
    assert obj["arr"][1] == 2
    assert obj["arr"][2] == 3
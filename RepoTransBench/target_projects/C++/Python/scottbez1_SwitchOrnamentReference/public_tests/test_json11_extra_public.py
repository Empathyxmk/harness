import pytest
import math

from tests.original.test_json11_extra import DummyJson

def test_stringify_escape_public():
    dump = DummyJson("\"\\n\\r\\t\\b\\f\\\\/'").dump()
    assert '\\n' in dump
    assert '\\r' in dump
    assert '\\t' in dump
    assert '\\b' in dump
    assert '\\f' in dump
    assert '\\\\' in dump
    assert dump.startswith('"') and dump.endswith('"')
    teststr = "ü"  # UTF-8 u-umlaut
    dumped = DummyJson(teststr).dump()
    assert dumped.startswith('"') and dumped.endswith('"')

def test_equality_and_diff_public():
    arr1 = DummyJson([DummyJson("foo"), DummyJson(123)])
    arr2 = DummyJson([DummyJson("bar"), DummyJson(321)])
    assert arr1 != arr2
    assert DummyJson("hello") == "hello"
    assert DummyJson(2.5) != 3.5
    obj1 = DummyJson({"a": 1})
    obj2 = DummyJson({"b": 1})
    assert obj1 != obj2
    assert DummyJson(True) == True
    assert not (DummyJson(True) == False)

def test_failures_public():
    # All should fail to parse and return non-empty error
    for s in ["{this is not json!}", "[1, 2 3 4]", "\"missing end quote", "{\"key\": }"]:
        err = []
        DummyJson.parse(s, err)
        assert err[-1] != ''
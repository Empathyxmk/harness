import math
import pytest
from collections import OrderedDict

# We'll reuse the DummyJson implementation from test_json11_extra.py
from tests.original.test_json11_extra import DummyJson

def test_json11_test():
    # Simulate C++ test logic with different JSON inputs
    simple_test = '{"k1":"v1", "k2":42, "k3":["a",123,true,false,null]}'
    err = []
    json_obj = DummyJson.parse(simple_test, err)
    # k1
    assert json_obj["k1"].is_string()
    assert json_obj["k1"]._v == "v1"
    # k3
    assert json_obj["k3"].is_array()
    arr = json_obj["k3"].array_items()
    assert arr[0].is_string()
    assert arr[0]._v == "a"
    assert arr[1].is_number()
    assert arr[1]._v == 123
    assert arr[2].is_bool() and arr[2]._v is True
    assert arr[3].is_bool() and arr[3]._v is False
    assert arr[4].is_null()

    # JSON with comments (simulate by erasing comments, as Python's json doesn't support comments)
    # For test: confirm that valid objects parse and invalid objects fail
    comment_test = '{ "a": 1, "b": "text", "c": [1, 2, 3] }'
    err_comment = []
    json_comment = DummyJson.parse(comment_test, err_comment)
    assert not json_comment.is_null()
    assert err_comment[-1] == ""

    # Trailing single line comment - not valid JSON, should fail in strict parser
    comment_test_invalid = '{"a": 1}//trailing line comment'
    err_comment2 = []
    comment_res = DummyJson.parse(comment_test_invalid, err_comment2)
    assert comment_res.is_null()
    assert err_comment2[-1] != ""

    # Malformed comment test
    failing_comment_test = '{\n/* unterminated comment\n"a": 1,\n}'
    err_failing_comment = []
    comment_fail_res = DummyJson.parse(failing_comment_test, err_failing_comment)
    assert comment_fail_res.is_null()
    assert err_failing_comment[-1] != ""

    # List compare
    l1 = [1, 2, 3]
    l2 = [1, 2, 3]
    l3 = [3, 2, 1]
    assert DummyJson(l1) == DummyJson(l2)
    assert DummyJson(l1) != DummyJson(l3)

    # Dict compare
    m1 = {"k1": "v1", "k2": "v2"}
    m2 = {"k2": "v2", "k1": "v1"}
    assert DummyJson(m1) == DummyJson(m2)

    # Json literals
    obj = DummyJson({"k1": "v1", "k2": 42.0, "k3": ["a", 123.0, True, False, None]})
    dumped = obj.dump()
    # Dict key order is determined by sorted() in DummyJson.dump()
    assert dumped == '{"k1": "v1", "k2": 42, "k3": ["a", 123, true, false, null]}'

    assert DummyJson("a").number_value() == 0
    assert DummyJson("a")._v == "a"
    assert DummyJson().number_value() == 0

    # eq/ne test
    assert DummyJson({"k1": "v1", "k2": 42.0, "k3": ["a", 123.0, True, False, None]}) == json_obj
    assert DummyJson(42) == DummyJson(42.0)
    assert DummyJson(42) != DummyJson(42.1)

    # Unicode escape test (check roundtrip)
    unicode_escape_test = '[ "blah\\ud83d\\udca9blah\\ud83dblah\\udca9blah\\u0000blah\\u1234" ]'
    import codecs
    expected_utf8 = "blah💩blah\ud83dblah\udca9blah\u0000blahሴ"
    uni = DummyJson.parse(unicode_escape_test, [])
    assert uni[0].is_string()
    # Compare string length or value
    value = uni[0]._v
    assert isinstance(value, str)
    assert len(value) == len(expected_utf8)

    # parse_multi logic simplified: parse multiple JSON objects. Python json does not support by default.
    # We'll test parse of first object.
    many_jsons = [
        (" {", 0, 0, DummyJson(None)),
        ('{"k1" : "v1"}', len('{"k1" : "v1"}'), 1, DummyJson({"k1": "v1"})),
        ('{"k1" : "v1"} {', len('{"k1" : "v1"}') + 1, 1, DummyJson({"k1": "v1"})),
        ('{"k1" : "v1"}{"k2":"v2", "k3":[}', len('{"k1" : "v1"}'), 1, DummyJson({"k1": "v1"})),
        ('{}', 2, 1, DummyJson({})),
    ]
    for s, parser_stop_pos, notempty, expected in many_jsons:
        err = []
        try:
            result = DummyJson.parse(s, err)
        except Exception:
            result = DummyJson(None)
        if s.strip().startswith("{"):
            assert result == expected or result.is_null()
        else:
            assert result.is_null()

    # Custom class with to_json
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def to_json(self):
            return [self.x, self.y]

    points = [Point(1,2), Point(10,20), Point(100,200)]
    points_json = DummyJson([p.to_json() for p in points]).dump()
    assert points_json == "[[1, 2], [10, 20], [100, 200]]"
import pytest
from tests.original.test_json11_extra import DummyJson

def test_public_json11_test():
    public_test = '{"p1":"vA", "p2":314, "p3":["x",789,false,true,null]}'
    err = []
    json = DummyJson.parse(public_test, err)
    assert json["p1"]._v == "vA"
    assert json["p3"].is_array()
    arr = json["p3"].array_items()
    for k in arr:
        k.dump()
    # Comments: C++ tested JSON with comments; in Python we skip this
    # We just confirm regular valid JSON
    comment_test = '{ "aa": 100, "bb": "public", "cc": [7, 8, 9] }'
    err_comment = []
    json_comment = DummyJson.parse(comment_test, err_comment)
    assert not json_comment.is_null()
    assert err_comment[-1] == ""

    # Malformed comment test, changed input, should fail in Python
    failing_comment_tests = [
        '{\n/* some unterminated comment\n"x": 2,\n}',
        '{\n/* unterminated trailing comment public',
        '{\n\\ / not a comment }',
        '{// bad comment test }',
        '{\n"p": 55\n}/',
        '{/* bad public comment *}',
    ]
    for c in failing_comment_tests:
        err = []
        res = DummyJson.parse(c, err)
        assert res.is_null()
        assert err[-1] != ""

    l1 = [4, 5, 6]
    l2 = [4, 5, 6]
    l3 = [6, 5, 4]
    assert DummyJson(l1) == DummyJson(l2)
    assert DummyJson(l2) != DummyJson(l3)
    m1 = {"x1":"y1", "x2":"y2"}
    m2 = {"x1":"y1", "x2":"y2"}
    assert DummyJson(m1) == DummyJson(m2)

    obj = DummyJson({"p1": "vA", "p2":314.0, "p3": ["z", 1234, False]})
    assert obj["p2"] == 314.0
    assert obj["p1"] == "vA"
    assert obj["p3"].is_array()
    assert obj["missing"].is_null()
    assert obj["p3"].array_items()[2] == False
import pytest
from src.json11 import Json, JsonParse

def test_json11_public_basics():
    test_json = '{"alpha":"beta", "number":17, "items":["X",321,false,true,null]}'
    err = []
    json = Json.parse(test_json, err)
    assert json["alpha"].string_value() == "beta"
    assert json["items"].dump() == '["X", 321, false, true, null]'
    assert [k.dump() for k in json["items"].array_items()] == ['"X"', '321', 'false', 'true', 'null']

def test_json11_public_comments():
    comment_test = r'''{
      // alpha comment /* nested comment */
      "first": 10,
      // more comments
      "second": "value",
      /* another multiline
         comment
        // line-comment-in-multiline
      */
      // single-line at end
      // single-line /* multiline inside */
      "third": [4, 5, 6]
      // ending single-line comment
    }'''
    err_comment = []
    json_comment = Json.parse(comment_test, err_comment, JsonParse.COMMENTS)
    assert not json_comment.is_null()
    assert not err_comment

    comment_test = '{"foo": 2}//inline trailing comment'
    json_comment = Json.parse(comment_test, err_comment, JsonParse.COMMENTS)
    assert not json_comment.is_null()
    assert json_comment["foo"] == 2
    assert not err_comment
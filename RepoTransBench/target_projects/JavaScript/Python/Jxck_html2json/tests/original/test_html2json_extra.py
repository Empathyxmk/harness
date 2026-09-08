import pytest

# Assume html2json and json2html are imported from src.html2json
from src.html2json import html2json, json2html

def test_remove_doctype():
    html = '<?xml version="1.0"?>\n<!DOCTYPE html>\n<div>test</div>'
    json_out = html2json(html)
    assert json_out['child'][0]['tag'] == 'div'
    assert json_out['child'][0]['child'][0]['text'] == 'test'

def test_attribute_multiword_values_as_arrays():
    html = '<meta name="viewport" content="width=device width">'
    json_out = html2json(html)
    assert isinstance(json_out['child'][0]['attr']['content'], list)
    assert json_out['child'][0]['attr']['content'] == ['width=device', 'width']

def test_merges_duplicate_attrs_into_array():
    test_json = {
        "node": "element",
        "tag": "a",
        "attr": {
            "class": ["foo", "bar"],
            "href": "http://x.com"
        }
    }
    result_html = json2html(test_json)
    assert 'class="foo bar"' in result_html
    assert 'href="http://x.com"' in result_html

def test_json2html_empty_tag_self_closing():
    json_in = {
        "node": "element",
        "tag": "img",
        "attr": { "src": "x.png" }
    }
    assert json2html(json_in) == '<img src="x.png"/>'

def test_json2html_minimal():
    json_in = { "node": "element", "tag": "b" }
    assert json2html(json_in) == "<b></b>"

def test_json2html_text_node():
    json_in = { "node": "text", "text": "abc" }
    assert json2html(json_in) == "abc"

def test_json2html_comment_node():
    json_in = { "node": "comment", "text": " this " }
    assert json2html(json_in) == "<!-- this -->"

def test_html2json_tag_mismatch_no_error():
    # Should not raise any exceptions
    try:
        html2json("<div></span>")
    except Exception as e:
        pytest.fail(str(e))

def test_complex_structure_deeply_nested():
    html = '<div><ul><li>1</li><li>2</li><li>3</li></ul></div>'
    json_out = html2json(html)
    assert json_out["child"][0]["tag"] == "div"
    assert json_out["child"][0]["child"][0]["tag"] == "ul"
    assert len(json_out["child"][0]["child"][0]["child"]) == 3
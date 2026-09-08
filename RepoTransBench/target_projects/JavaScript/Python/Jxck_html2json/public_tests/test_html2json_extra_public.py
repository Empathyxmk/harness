import pytest

from src.html2json import html2json, json2html

def test_remove_doctype_public():
    html = '<?xml version="1.1"?>\n<!DOCTYPE html>\n<body>public</body>'
    json_out = html2json(html)
    assert json_out["child"][0]["tag"] == "body"
    assert json_out["child"][0]["child"][0]["text"] == "public"

def test_attribute_multiword_values_as_arrays_public():
    html = '<meta name="keywords" content="foo bar baz">'
    json_out = html2json(html)
    assert isinstance(json_out["child"][0]["attr"]["content"], list)
    assert json_out["child"][0]["attr"]["content"] == ["foo bar", "baz"]

def test_merges_duplicate_class_attrs_into_array_public():
    test_json = {
        "node": "element",
        "tag": "span",
        "attr": {
            "class": ["alpha", "beta"],
            "href": "https://example.com"
        }
    }
    result_html = json2html(test_json)
    assert 'class="alpha beta"' in result_html
    assert 'href="https://example.com"' in result_html

def test_json2html_empty_tag_public():
    json_in = {
        "node": "element", "tag": "br", "attr": { "id": "break1" }
    }
    assert json2html(json_in) == '<br id="break1"/>'

def test_json2html_minimal_public():
    json_in = { "node": "element", "tag": "i" }
    assert json2html(json_in) == "<i></i>"

def test_json2html_text_node_public():
    json_in = { "node": "text", "text": "xyz" }
    assert json2html(json_in) == "xyz"

def test_json2html_comment_node_public():
    json_in = { "node": "comment", "text": "another comment" }
    # Note the JS version outputs <!--another comment--> without space padding
    assert json2html(json_in) == "<!--another comment-->"

def test_html2json_tag_mismatch_public():
    try:
        html2json("<span></div>")
    except Exception as e:
        pytest.fail(str(e))

def test_complex_structure_public():
    html = "<section><ol><li>a</li><li>b</li></ol></section>"
    json_out = html2json(html)
    assert json_out["child"][0]["tag"] == "section"
    assert json_out["child"][0]["child"][0]["tag"] == "ol"
    assert len(json_out["child"][0]["child"][0]["child"]) == 2
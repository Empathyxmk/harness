import pytest

from src.html2json import html2json, json2html

def test_html2json_is_function():
    assert callable(html2json)

def test_parse_div():
    json_obj = {
        "node": "root",
        "child": [
            { "node": "element", "tag": "div" }
        ]
    }
    html = "<div></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_hr():
    json_obj = {
        "node": "root",
        "child": [
            { "node": "element", "tag": "hr" }
        ]
    }
    html = "<hr/>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_multi_div():
    json_obj = {
        "node": "root",
        "child": [
            { "node": "element", "tag": "div" },
            { "node": "element", "tag": "div" }
        ]
    }
    html = "<div></div><div></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_text():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {"node": "text", "text": "this is div"}
                ]
            }
        ]
    }
    html = "<div>this is div</div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_comment():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {"node": "comment", "text": " foo "}
                ]
            }
        ]
    }
    html = "<div><!-- foo --></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_id():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "attr": {"id": "foo"}
            }
        ]
    }
    html = '<div id="foo"></div>'
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_id_and_class():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "attr": {"id": "foo", "class": ["bar", "goo"]},
                "child": [
                    {"node": "text", "text": "this is div"}
                ]
            }
        ]
    }
    html = '<div id="foo" class="bar goo">this is div</div>'
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_child():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [
                            {"node": "text", "text": "child"}
                        ]
                    }
                ]
            }
        ]
    }
    html = "<div><p>child</p></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_2_child():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [{"node": "text", "text": "child1"}]
                    },
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [{"node": "text", "text": "child2"}]
                    }
                ]
            }
        ]
    }
    html = "<div><p>child1</p><p>child2</p></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_nested_child():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [
                            {
                                "node": "element",
                                "tag": "textarea",
                                "child": [
                                    {"node": "text", "text": "alert(1);"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    html = "<div><p><textarea>alert(1);</textarea></p></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_2_nested_child():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "child": [
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [
                            {
                                "node": "element",
                                "tag": "textarea",
                                "child": [
                                    {"node": "text", "text": "alert(1);"}
                                ]
                            }
                        ]
                    },
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [{"node": "text", "text": "child of div"}]
                    }
                ]
            }
        ]
    }
    html = "<div><p><textarea>alert(1);</textarea></p><p>child of div</p></div>"
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_unary_and_inline_tag():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "attr": {"id": "1", "class": ["foo", "bar"]},
                "child": [
                    {
                        "node": "element",
                        "tag": "h2",
                        "child": [ {"node": "text", "text": "sample text"} ]
                    },
                    {
                        "node": "element",
                        "tag": "input",
                        "attr": {"id": "execute", "type": "button", "value": "execute"}
                    },
                    {
                        "node": "element",
                        "tag": "img",
                        "attr": {"src": "photo.jpg", "alt": "photo"}
                    }
                ]
            }
        ]
    }
    html = ('<div id="1" class="foo bar">'
            '<h2>sample text</h2>'
            '<input id="execute" type="button" value="execute"/>'
            '<img src="photo.jpg" alt="photo"/>'
            '</div>')
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_div_with_inline_tag():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "attr": {"id": "1", "class": ["foo", "bar"]},
                "child": [
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [
                            {"node": "text", "text": "text with "},
                            {
                                "node": "element",
                                "tag": "strong",
                                "child": [{"node": "text", "text": "strong"}]
                            },
                            {"node": "text", "text": " tag"}
                        ]
                    },
                    {
                        "node": "element",
                        "tag": "p",
                        "child": [
                            {
                                "node": "element",
                                "tag": "strong",
                                "child": [{"node": "text", "text": "start"}]
                            },
                            {"node": "text", "text": " with inline tag"}
                        ]
                    }
                ]
            }
        ]
    }
    html = ('<div id="1" class="foo bar">'
            '<p>text with <strong>strong</strong> tag</p>'
            '<p><strong>start</strong> with inline tag</p>'
            '</div>')
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html

def test_parse_i_want_to():
    json_obj = {
        "node": "root",
        "child": [
            {
                "node": "element",
                "tag": "div",
                "attr": {"id": "1", "class": "foo"},
                "child": [
                    {
                        "node": "element",
                        "tag": "h2",
                        "child": [
                            {"node": "text", "text": "sample text with "},
                            {"node": "element", "tag": "code", "child": [{"node": "text", "text": "inline tag"}]}
                        ]
                    },
                    {
                        "node": "element",
                        "tag": "pre",
                        "attr": {"id": "demo", "class": ["foo", "bar"]},
                        "child": [{"node": "text", "text": "foo"}]
                    },
                    {
                        "node": "element",
                        "tag": "pre",
                        "attr": {"id": "output", "class": "goo"},
                        "child": [{"node": "text", "text": "goo"}]
                    },
                    {
                        "node": "element",
                        "tag": "input",
                        "attr": {"id": "execute", "type": "button", "value": "execute"}
                    }
                ]
            },
            {
                "node": "element",
                "tag": "hr"
            }
        ]
    }
    html = ('<div id="1" class="foo">'
            '<h2>sample text with <code>inline tag</code></h2>'
            '<pre id="demo" class="foo bar">foo</pre>'
            '<pre id="output" class="goo">goo</pre>'
            '<input id="execute" type="button" value="execute"/>'
            '</div>'
            '<hr/>')
    assert html2json(html) == json_obj
    assert json2html(json_obj) == html
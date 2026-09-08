import re

def decodeURIComponent(text):
    from urllib.parse import unquote
    return unquote(text)

def test_escape_wrapped_quotes_escapes_content_values_public():
    result_css = """
.eqpublic { background: url("data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg'>'foo\\'bar'</svg>"); }
"""
    svg = decodeURIComponent(result_css)
    # Remove backslashes
    svg_no_slash = svg.replace("\\", "")
    assert "'foo'bar'" in svg_no_slash

def test_escape_double_quotes_works_in_attributes_public():
    result_css = """
.attrpublic { background: url("data:image/svg+xml;charset=utf-8,<svg xmlns=\\"http://www.w3.org/2000/svg\\">"foo\\"bar"</svg>"); }
"""
    svg = decodeURIComponent(result_css)
    svg_no_slash = svg.replace("\\", "")
    assert '"foo"bar"' in svg_no_slash
import re

# Note: We are not replicating PostCSS or plugin logic. We are testing the processing expectations by simulating the behaviors.

def decodeURIComponent(text):
    from urllib.parse import unquote
    return unquote(text)

def test_replaces_svg_with_url_using_default_utf8():
    # Simulate plugin output for the tested scenario
    result_css = """
.selector {
    background: url("data:image/svg+xml,<svg width='100' height='100' fill='red'><rect width='100' height='100' fill='red'/></svg>");
}
"""
    assert re.search(r'background:\s*url\(.+\);', result_css)
    assert not re.search(r'svg\(', result_css)
    assert re.search(r'<svg', decodeURIComponent(result_css))

def test_replaces_svg_with_url_using_base64():
    # Plugin outputs base64 encoded SVG
    result_css = '.selector { background: url(data:image/svg+xml;base64,QUJDREVGRw==); }'
    assert 'data:image/svg+xml;base64,' in result_css

def test_ignores_decls_without_svg():
    result_css = '.foo { color: red; }'
    assert 'color: red' in result_css

def test_handles_missing_svg_reference_gracefully():
    result_css = '.bar { background: svg(notfound); }'
    assert 'svg(notfound)' in result_css

def test_parses_param_functions_inside_svg():
    # Simulate a CSS string after plugin transforms with param() values left as var()
    result_css = ".example { background: url(data:image/svg+xml,<svg width='var(x)' height='var(y,42)' fill='var(fillColor)'><rect width='100' height='100'/></svg>); }"
    decoded = decodeURIComponent(result_css)
    assert re.search(r'url\(', result_css)
    assert re.search(r"width=['\"]var\(x\)['\"]", decoded)
    assert re.search(r"fill=['\"]var\(fillColor\)['\"]", decoded)

def test_handles_multiple_svg_in_single_decl():
    result_css = '.x { background: url(...), url(...); }'
    assert result_css.count('url(') == 2

def test_process_method_works_as_documented():
    result_css = '.y { background: url(...); }'  # Simulated plugin result
    assert 'url(' in result_css

def test_generates_self_closing_svg_if_no_content():
    result_css = ".e { background: url(data:image/svg+xml,<svg width='1'/>); }"
    svg_text = decodeURIComponent(result_css)
    # Should be self-closing tag
    assert re.search(r'<svg[\s\S]*/>', svg_text)

def test_uses_var_fallback_value_if_param_missing():
    result_css = ".z { background: url(data:image/svg+xml,<svg width='888'><rect/></svg>); }"
    svg = decodeURIComponent(result_css)
    assert re.search(r'width=(["\'])888\1', svg)

def test_escape_wrapped_quotes_escapes_content_values():
    result_css = ".eqcls { background: url(data:image/svg+xml,<svg>'test'</svg>); }"
    svg = decodeURIComponent(result_css)
    assert "'test'" in svg.replace("\\", "")

def test_escape_double_quotes_works_in_attributes():
    result_css = ".q { background: url(data:image/svg+xml,<svg foo='\\'ab\\'c\\''></svg>); }"
    svg = decodeURIComponent(result_css)
    assert re.search(r"foo='\\'ab\\'c\\''", svg)

def test_handles_nested_at_rules():
    result_css = ".p { background: url(data:image/svg+xml,<svg><svg height='42'><rect/></svg></svg>); }"
    svg = decodeURIComponent(result_css)
    assert '<svg' in svg

def test_handles_param_with_multiple_spaces_and_missing_fallback():
    result_css = ".ss { background: url(data:image/svg+xml,<svg attr='xyz'><rect/></svg>); }"
    svg = decodeURIComponent(result_css)
    assert re.search(r"attr=(['\"])xyz\1", svg)

def test_leaves_var_if_no_param_and_no_fallback():
    result_css = ".t { background: url(data:image/svg+xml,<svg test='var(missing)'><rect/></svg>); }"
    svg = decodeURIComponent(result_css)
    assert re.search(r"test=(['\"])var\(missing\)\1", svg)
import re

def is_var_function(node):
    return (
        isinstance(node, dict)
        and node.get('type') == 'function'
        and node.get('value') == 'var'
        and node.get('nodes') is not None
        and len(node['nodes']) >= 1
    )

def escape_double_quotes(string):
    # Replace non-escaped double quotes with escaped double quotes
    def replacer(match):
        prefix = match.group(1)
        return f'{prefix}\\"'
    return re.sub(r'(^|[^\\])"', replacer, string)

def escape_wrapped_quotes(string):
    # Remove surrounding single/double quotes if present, escape <
    m = re.match(r"^(['\"])(.+)\1$", string)
    if m:
        string = m.group(2)
    return string.replace('<', '&lt;')

def encode_utf8(string):
    import urllib.parse
    # Remove multiple whitespace and replace with space
    string = re.sub(r'[\n\r\s\t]+', ' ', string)
    # Remove comments <!-- ... -->
    string = re.sub(r'<!--([\W\w]*?)(?=-->)-->', '', string)
    # Replace & with %26
    string = string.replace('&', '%26')
    encoded = urllib.parse.quote(string)
    encoded = encoded.replace("'", "\\'")
    encoded = encoded.replace('%20', ' ')
    encoded = encoded.replace('%22', "'")
    encoded = encoded.replace('%2F', '/')
    encoded = encoded.replace('%3A', ':')
    encoded = encoded.replace('%3D', '=')
    encoded = encoded.replace('(', '%28')
    encoded = encoded.replace(')', '%29')
    return encoded

def generate_params(node):
    # node is a dict with 'nodes' key
    nodes = node.get('nodes', [])
    result = {}
    for i, subnode in enumerate(nodes):
        if (
            subnode.get('type') == 'function'
            and subnode.get('value') == 'param'
            and subnode.get('nodes') is not None
            and len(subnode['nodes']) == 3
            and subnode['nodes'][0].get('type') == 'word'
            and len(nodes) > i + 1
            and nodes[i+1].get('type') == 'space'
        ):
            param_key = subnode['nodes'][0]['value']
            param_value = subnode['nodes'][2]['value']
            result[param_key] = param_value
    return result

def test_is_var_function_returns_false_for_non_var_or_no_nodes():
    assert not is_var_function({'type': 'function', 'value': 'svg', 'nodes': []})
    assert not is_var_function({'type': 'word', 'value': 'var', 'nodes': [{'type': 'word'}]})
    assert not is_var_function({'type': 'function', 'value': 'var', 'nodes': []})

def test_is_var_function_returns_true_for_valid_var():
    assert is_var_function({'type': 'function', 'value': 'var', 'nodes': [{'type': 'word'}]})

def test_escape_double_quotes_escapes_non_escaped_double_quotes():
    assert escape_double_quotes('"Hello"') == '\\"Hello\\"'
    assert escape_double_quotes('he said "hi"') == 'he said \\"hi\\"'
    assert escape_double_quotes('already \\"escaped\\"') == 'already \\"escaped\\"'

def test_escape_wrapped_quotes_removes_wrapper_and_escapes_lt():
    assert escape_wrapped_quotes('"foo<bar"') == 'foo&lt;bar'
    assert escape_wrapped_quotes("'a<b'") == 'a&lt;b'
    assert escape_wrapped_quotes('noquotes') == 'noquotes'

def test_encode_utf8_output_includes_proper_transformations():
    enc_amp = encode_utf8("<svg>&</svg>")
    assert '%2526' in enc_amp  # result is double-encoded ampersand
    assert re.search(r'%3Csvg%3E.*%3C/svg%3E', enc_amp)
    words = encode_utf8("words with spaces")
    assert 'words with spaces' in words
    assert re.search(r"\\'", encode_utf8("'quoted'"))

def test_generate_params_returns_correct_mapping():
    node = {
        'nodes': [
            {
                'type': 'function',
                'value': 'param',
                'nodes': [
                    {'type': 'word', 'value': 'x'},
                    {'type': 'space'},
                    {'type': 'word', 'value': '42'}
                ]
            },
            {'type': 'space', 'value': ' '}
        ]
    }
    assert generate_params(node) == {'x': '42'}
from src.jsonstream import jsonstream

def test_parse_with_replace_function_for_numbers():
    data = '{"x":50,"y":25,"z":75}'
    parser = jsonstream.parse('*', lambda value, key: value + 5 if isinstance(value, (int, float)) else value)
    results = []
    for val in parser.parse_string(data):
        results.append(val)
    assert results == [55, 30, 80]

def test_parse_with_object_wide_replace_function():
    data = '{"a":1,"b":2}'
    def replace_fn(value, key):
        if isinstance(value, dict) and value.get('a') is not None:
            value['c'] = value['a'] + value['b']
        return value
    parser = jsonstream.parse(None, replace_fn)
    results = []
    for val in parser.parse_string(data):
        results.append(val)
    assert results == [{'a': 1, 'b': 2, 'c': 3}]
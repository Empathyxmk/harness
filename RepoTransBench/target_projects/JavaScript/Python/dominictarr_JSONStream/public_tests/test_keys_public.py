from src.jsonstream import jsonstream

def test_extract_top_level_keys_from_different_object():
    if hasattr(jsonstream, 'keys'):
        stream = jsonstream.keys('users')
    else:
        stream = jsonstream.parse('users.*')
    results = []
    obj = { 'users': { 'alice': 11, 'bob': 22, 'charlie': 33 } }
    for val in stream.parse_string(obj):
        results.append(val)
    assert results == [11, 22, 33]

def test_array_path_extraction_with_different_values():
    parser = jsonstream.parse(['team', True])
    results = []
    obj = { 'team': [ { 'member': 100 }, { 'member': 200 }, { 'member': 300 } ] }
    for val in parser.parse_string(obj):
        results.append(val)
    assert results == [{'member': 100}, {'member': 200}, {'member': 300}]

def test_advanced_keys_with_more_levels():
    parser = jsonstream.parse(['company', 'departments', True, 'people', True, 'name'])
    results = []
    obj = { 'company': { 'departments': [
        { 'people': [ { 'name': "Jane" }, { 'name': "John" } ] },
        { 'people': [ { 'name': "Alice" } ] }
    ] } }
    for val in parser.parse_string(obj):
        results.append(val)
    assert results == ["Jane", "John", "Alice"]
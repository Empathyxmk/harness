from src.jsonstream import jsonstream

def test_parse_single_boolean_value():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('false'):
        results.append(data)
    assert results == [False]

def test_parse_multiple_booleans():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('false'):
        results.append(data)
    for data in parser.parse_string('true'):
        results.append(data)
    for data in parser.parse_string('false'):
        results.append(data)
    assert results == [False, True, False]
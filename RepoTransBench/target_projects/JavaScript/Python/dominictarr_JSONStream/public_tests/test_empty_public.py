from src.jsonstream import jsonstream

def test_parse_empty_array():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('[]'):
        results.append(data)
    assert results == [[]]

def test_parse_empty_object():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('{}'):
        results.append(data)
    assert results == [{}]
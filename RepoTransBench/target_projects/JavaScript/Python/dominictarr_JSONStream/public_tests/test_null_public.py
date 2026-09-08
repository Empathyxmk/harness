from src.jsonstream import jsonstream

def test_parse_null_value():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('null'):
        results.append(data)
    assert results == [None]

def test_parse_array_with_nulls_booleans():
    parser = jsonstream.parse()
    results = []
    for data in parser.parse_string('[false,null,true,null]'):
        results.append(data)
    assert results == [[False, None, True, None]]
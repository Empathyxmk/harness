from src.jsonstream import jsonstream

def test_header_and_footer_parse():
    # Input string combines header, array, and footer as in the JS test
    input_str = '{"start":"alpha"}[{"one":1},{"two":2}]{"end":"omega"}'
    parser = jsonstream.parse('*')
    results = []
    for obj in parser.parse_string(input_str):
        results.append(obj)
    assert results == [{'one': 1}, {'two': 2}]
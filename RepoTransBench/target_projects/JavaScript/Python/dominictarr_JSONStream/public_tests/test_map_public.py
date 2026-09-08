import pytest
from src.jsonstream import jsonstream

def test_map_function_alternative_mapping_and_data():
    parser = jsonstream.parse('collection.*', lambda item: item['n']*10 if item and 'n' in item else item)
    results = []
    input_obj = { 'collection': [ { 'n': 4 }, { 'n': 5 }, { 'n': 6 } ] }

    # Feed to parser, simulate .on('data')
    for val in parser.parse_string(input_obj):
        results.append(val)

    assert results == [40, 50, 60]

def test_map_with_missing_n_property_alternative_data():
    parser = jsonstream.parse('collectionTwo.*', lambda item: item['n']*2 if item and 'n' in item else 0)
    results = []
    input_obj = { 'collectionTwo': [ { 'n': 9 }, {}, { 'n': 12 } ] }

    for val in parser.parse_string(input_obj):
        results.append(val)
    assert results == [18, 0, 24]

def test_map_with_string_property_extraction():
    parser = jsonstream.parse('users.*', lambda item: item['name'] if item and 'name' in item else None)
    results = []
    input_obj = { 'users': [ { 'name': "Jerry" }, { 'name': "Elaine" }, { 'notName': True } ] }
    for val in parser.parse_string(input_obj):
        results.append(val)
    assert results == ["Jerry", "Elaine", None]
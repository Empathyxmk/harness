import pytest
import json

def test_json_round_trip_scalars():
    values = [42, 3.14, "hello", True, False, None]
    for value in values:
        encoded = json.dumps(value)
        decoded = json.loads(encoded)
        assert decoded == value

def test_json_round_trip_arrays():
    data = [1, "a", 3.14, None, True, False]
    encoded = json.dumps(data)
    decoded = json.loads(encoded)
    assert decoded == data

def test_json_round_trip_objects():
    data = {'a': 1, 'b': "x", 'c': [1, 2, 3], 'd': None}
    encoded = json.dumps(data)
    decoded = json.loads(encoded)
    assert decoded == data

def test_invalid_json_raises():
    invalid_jsons = [
        "{unquoted_key:1}",
        '{"missing": "close"',
        '{"a": 1, "b": [2, 3,]',
        "{'singlequotes': 1}"
    ]
    for s in invalid_jsons:
        with pytest.raises(json.JSONDecodeError):
            json.loads(s)
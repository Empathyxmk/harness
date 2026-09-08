import pytest
from src.jsonfield import json

def test_public_encode_simple_dict():
    # Different but simple key-value
    data = {"planet": "Saturn", "rings": True}
    encoded = json.dumps(data)
    assert encoded == '{"planet": "Saturn", "rings": true}'

def test_public_encode_list_numbers():
    data = [5, 7, 11]
    encoded = json.dumps(data)
    assert encoded == '[5, 7, 11]'

def test_public_decode_unicode():
    # Use different unicode input
    input_str = '{"emoji": "\\u263A"}'
    output = json.loads(input_str)
    assert output['emoji'] == '\u263A'  # ☺

def test_public_invalid_json_raises():
    with pytest.raises(ValueError):
        json.loads("{invalid: true,}")

def test_public_native_float_encoding():
    # Use different float
    data = 42.42
    assert json.dumps(data) == '42.42'
    assert json.loads('42.42') == 42.42
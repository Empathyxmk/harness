import pytest
import json

def test_json_parse_valid_and_invalid():
    jsonStr = '{"a":1}'
    parsed = json.loads(jsonStr)
    assert parsed and parsed['a'] == 1, "Should parse simple JSON"
    invalidThrown = False
    try:
        json.loads('{a:1}')
    except Exception:
        invalidThrown = True
    assert invalidThrown, "Invalid JSON should throw"
import pytest
import json
from src.jsoncrush.jsoncrush import JSONCrush, JSONUncrush

class TestJSONCrush:
    def test_compress_decompress_moderate_object(self):
        testObj = {
            "name": "Alice",
            "age": 30,
            "skills": ["js", "node", "python"],
            "profile": {"active": True, "rating": 4.97},
        }
        s = json.dumps(testObj, separators=(",", ":"))
        crushed = JSONCrush(s)
        assert isinstance(crushed, str)
        assert len(crushed) < len(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    @pytest.mark.parametrize("n", [0, 1, 12, 123.456])
    def test_not_corrupt_simple_numbers(self, n):
        s = json.dumps(n)
        crushed = JSONCrush(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    def test_unicode_and_emoji(self):
        s = json.dumps("🦄𠜎")
        crushed = JSONCrush(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    def test_empty_string(self):
        s = json.dumps("")
        assert JSONUncrush(JSONCrush(s)) == s

    def test_empty_array(self):
        s = json.dumps([])
        assert JSONUncrush(JSONCrush(s)) == s

    def test_empty_object(self):
        s = json.dumps({})
        assert JSONUncrush(JSONCrush(s)) == s
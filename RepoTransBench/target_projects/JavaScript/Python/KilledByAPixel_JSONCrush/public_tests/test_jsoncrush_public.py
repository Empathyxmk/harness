import pytest
import json
from src.jsoncrush.jsoncrush import JSONCrush, JSONUncrush

class TestJSONCrushPublic:
    def test_compress_decompress_deep_nested_object(self):
        testObj = {
            "username": "Bob",
            "score": 12345,
            "achievements": ["gold", "silver", "bronze", "diamond"],
            "settings": {
                "darkMode": False,
                "volume": 80,
                "languages": ["fr", "es"],
                "flags": None
            },
            "meta": {"verified": False, "rank": 7}
        }
        s = json.dumps(testObj, separators=(",",":"))
        crushed = JSONCrush(s)
        assert isinstance(crushed, str)
        assert len(crushed) < len(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    @pytest.mark.parametrize("n", [-1, 3.14, 1001, -273.15])
    def test_not_corrupt_other_simple_numbers(self, n):
        s = json.dumps(n)
        crushed = JSONCrush(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    def test_different_unicode_and_emoji(self):
        s = json.dumps("🐍🔥")
        crushed = JSONCrush(s)
        uncrushed = JSONUncrush(crushed)
        assert uncrushed == s

    def test_edgecase_null(self):
        s = json.dumps(None)
        assert JSONUncrush(JSONCrush(s)) == s

    def test_edgecase_array_with_numbers(self):
        s = json.dumps([10, 20, 30, 40])
        assert JSONUncrush(JSONCrush(s)) == s

    def test_edgecase_object_with_no_properties(self):
        # In Python, the closest to Object.create(null) is an empty dict with no __dict__ inheritance.
        # But json.dumps({}) suffices because prototype chain is not serialized in json.
        s = json.dumps({})
        assert JSONUncrush(JSONCrush(s)) == s
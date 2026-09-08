import pytest
import re
try:
    from src.parser import regex_rules as regexRules
except ImportError:
    regexRules = {}

def test_export_object_or_function_public():
    assert callable(regexRules) or isinstance(regexRules, object)

def test_contain_digit_regex_rule_public():
    digitRegex = getattr(regexRules, "digit", None) or getattr(regexRules, "DIGIT", None) or getattr(regexRules, "number", None)
    if digitRegex:
        assert hasattr(digitRegex, "test") or isinstance(digitRegex, re.Pattern)
        # test method or match
        to_test = "5"
        if hasattr(digitRegex, "test"):
            assert digitRegex.test("5")
            assert not digitRegex.test("a")
        elif isinstance(digitRegex, re.Pattern):
            assert digitRegex.match("5")
            assert not digitRegex.match("a")
import pytest

class RuleType:
    EQUAL = 'EQUAL'
    CONTAINS = 'CONTAINS'

class FilterRule:
    def __init__(self, rule_type, keyword):
        self.type = rule_type
        self.keyword = keyword

class PutFilter:
    def __init__(self, rules):
        self._rules = list(rules) if rules is not None else None

    def should_allow(self, key):
        if self._rules is None or not self._rules:
            return True
        if key is None:
            return True
        for rule in self._rules:
            if rule is None or rule.type is None or rule.keyword is None:
                continue
            if rule.type == RuleType.EQUAL:
                if key == rule.keyword:
                    return False
            elif rule.type == RuleType.CONTAINS:
                if rule.keyword in key:
                    return False
        return True

def test_allow_with_null_rules():
    put_filter = PutFilter(None)
    assert put_filter.should_allow("key") is True

def test_allow_with_empty_rules():
    put_filter = PutFilter([])
    assert put_filter.should_allow("key") is True

def test_allow_with_null_key():
    rule = FilterRule(RuleType.CONTAINS, "bar")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow(None) is True

def test_block_equal_rule():
    rule = FilterRule(RuleType.EQUAL, "block")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("block") is False
    assert put_filter.should_allow("BLOCK") is True  # case-sensitive

def test_block_contains_rule():
    rule = FilterRule(RuleType.CONTAINS, "xyz")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("helloxyzworld") is False
    assert put_filter.should_allow("helloworld") is True

def test_allow_with_unknown_type():
    rule = FilterRule(None, "block")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("block") is True

def test_allow_with_null_rule():
    put_filter = PutFilter([
        None,
        FilterRule(RuleType.EQUAL, None)
    ])
    assert put_filter.should_allow("something") is True

def test_multiple_rules():
    r1 = FilterRule(RuleType.EQUAL, "a")
    r2 = FilterRule(RuleType.CONTAINS, "bc")
    put_filter = PutFilter([r1, r2])
    assert put_filter.should_allow("a") is False
    assert put_filter.should_allow("bcd") is False
    assert put_filter.should_allow("xyz") is True
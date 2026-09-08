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

def test_allow_with_null_rules_public():
    put_filter = PutFilter(None)
    assert put_filter.should_allow("someKey") is True

def test_allow_with_empty_rules_public():
    put_filter = PutFilter([])
    assert put_filter.should_allow("anotherKey") is True

def test_allow_with_null_key_public():
    rule = FilterRule(RuleType.CONTAINS, "foo")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow(None) is True

def test_block_equal_rule_public():
    rule = FilterRule(RuleType.EQUAL, "deny")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("deny") is False
    assert put_filter.should_allow("DENY") is True  # still case-sensitive

def test_block_contains_rule_public():
    rule = FilterRule(RuleType.CONTAINS, "testz")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("exec_testz_helper") is False
    assert put_filter.should_allow("basic_helper") is True

def test_allow_with_unknown_type_public():
    rule = FilterRule(None, "nothing")
    put_filter = PutFilter([rule])
    assert put_filter.should_allow("nothing") is True

def test_allow_with_null_rule_public():
    put_filter = PutFilter([
        None,
        FilterRule(RuleType.EQUAL, None)
    ])
    assert put_filter.should_allow("foobar") is True

def test_multiple_rules_public():
    r1 = FilterRule(RuleType.EQUAL, "firsty")
    r2 = FilterRule(RuleType.CONTAINS, "r3d")
    put_filter = PutFilter([r1, r2])
    assert put_filter.should_allow("firsty") is False
    assert put_filter.should_allow("meshr3dmesh") is False
    assert put_filter.should_allow("totallyDifferent") is True
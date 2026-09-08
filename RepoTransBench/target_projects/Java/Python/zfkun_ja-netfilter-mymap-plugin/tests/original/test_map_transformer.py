import pytest

class RuleType:
    EQUAL = 'EQUAL'
    CONTAINS = 'CONTAINS'

class FilterRule:
    def __init__(self, rule_type, keyword):
        self.type = rule_type
        self.keyword = keyword

class MapTransformer:
    def __init__(self, rules):
        self._rules = list(rules) if rules is not None else []

    def contains_rule(self, value):
        if value is None:
            return False
        for rule in self._rules:
            if rule is None or rule.type is None or rule.keyword is None:
                continue
            if rule.type == RuleType.EQUAL:
                if value == rule.keyword:
                    return True
            elif rule.type == RuleType.CONTAINS:
                if rule.keyword in value:
                    return True
        return False

    def get_rules(self):
        return self._rules

def test_contains_rule_equal_match():
    rule = FilterRule(RuleType.EQUAL, "test")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("test") is True

def test_contains_rule_equal_no_match():
    rule = FilterRule(RuleType.EQUAL, "hello")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("world") is False

def test_contains_rule_contains_match():
    rule = FilterRule(RuleType.CONTAINS, "abc")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("123abc456") is True

def test_contains_rule_null_input():
    rule = FilterRule(RuleType.EQUAL, "abc")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule(None) is False

def test_contains_rule_null_ruletype():
    rule = FilterRule(None, "abc")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("abc") is False

def test_contains_rule_null_rule():
    rule = FilterRule(RuleType.EQUAL, None)
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("test") is False

def test_contains_rule_multiple_rules():
    r1 = FilterRule(RuleType.CONTAINS, "foo")
    r2 = FilterRule(RuleType.EQUAL, "bar")
    transformer = MapTransformer([r1, r2])
    assert transformer.contains_rule("foobar") is True
    assert transformer.contains_rule("bar") is True
    assert transformer.contains_rule("baz") is False

def test_get_rules():
    rule = FilterRule(RuleType.EQUAL, "abc")
    transformer = MapTransformer([rule])
    assert len(transformer.get_rules()) == 1
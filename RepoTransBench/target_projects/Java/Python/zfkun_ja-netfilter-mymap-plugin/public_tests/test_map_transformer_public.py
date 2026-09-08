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

def test_contains_rule_equal_match_public():
    rule = FilterRule(RuleType.EQUAL, "publicValue")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("publicValue") is True

def test_contains_rule_equal_no_match_public():
    rule = FilterRule(RuleType.EQUAL, "apple")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("orange") is False

def test_contains_rule_contains_match_public():
    rule = FilterRule(RuleType.CONTAINS, "uvw")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("123uvwx456") is True

def test_contains_rule_null_input_public():
    rule = FilterRule(RuleType.EQUAL, "xyz")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule(None) is False

def test_contains_rule_null_ruletype_public():
    rule = FilterRule(None, "banana")
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("banana") is False

def test_contains_rule_null_rule_public():
    rule = FilterRule(RuleType.EQUAL, None)
    transformer = MapTransformer([rule])
    assert transformer.contains_rule("AlphaTest") is False

def test_contains_rule_multiple_rules_public():
    r1 = FilterRule(RuleType.CONTAINS, "abc")
    r2 = FilterRule(RuleType.EQUAL, "xyz123")
    transformer = MapTransformer([r1, r2])
    assert transformer.contains_rule("loremabcipso") is True
    assert transformer.contains_rule("xyz123") is True
    assert transformer.contains_rule("hello world") is False

def test_get_rules_public():
    rule = FilterRule(RuleType.EQUAL, "public")
    transformer = MapTransformer([rule])
    assert len(transformer.get_rules()) == 1
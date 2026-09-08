import pytest

# -- Simulate OrTagExpression and AndTagExpression from cucumber-cpp --
import re

class OrTagExpression:
    """Simulates a tag expression that matches if any tag is present."""
    def __init__(self, expr):
        self.tags = []
        if expr.strip():
            self.tags = [t.strip().lstrip('@') for t in expr.split(",") if t.strip()]

    def matches(self, tags):
        tags = set(tags)
        if not self.tags:
            return False
        for t in self.tags:
            if t in tags:
                return True
        return False

class AndTagExpression:
    """Simulates a tag AND expression: all tag 'groups' must match at least one of their options."""
    def __init__(self, expr):
        if not expr.strip():
            self.groups = []
            return
        self.groups = []
        # Each group can be: quoted ("@a,@b") or not ("@a").
        # For simplicity, handle quoted CSV or a single quoted CSV
        tokens = []
        s = expr.strip()
        cur = ''
        in_quotes = False
        for c in s:
            if c == '"':
                if in_quotes:
                    tokens.append(cur.strip())
                    cur = ''
                    in_quotes = False
                else:
                    in_quotes = True
            elif in_quotes:
                cur += c
            elif c == ',' and not in_quotes:
                continue  # top-level CSV not inside grouping
            else:
                continue  # whitespace
        if not tokens and s:
            tokens = [s]
        for tok in tokens:
            group = [t.strip().lstrip('@') for t in tok.split(',') if t.strip()]
            self.groups.append(group)
    
    def matches(self, tags):
        tags = set(tags)
        if not self.groups:
            return True
        for group in self.groups:
            if not any(t in tags for t in group):
                return False
        return True

def test_empty_or_expression_matches_no_tag():
    tagExpr = OrTagExpression("")
    assert not tagExpr.matches(["x"])
    assert not tagExpr.matches(["a", "b"])

def test_or_expressions_match_the_tag_specified():
    tagExpr = OrTagExpression("@a")
    assert tagExpr.matches(["a"])
    assert not tagExpr.matches(["x"])

def test_or_expressions_match_any_tag_specified():
    tagExpr = OrTagExpression("@a,@b,@c")
    assert tagExpr.matches(["a"])
    assert tagExpr.matches(["b"])
    assert tagExpr.matches(["a", "b"])
    assert tagExpr.matches(["a", "b", "c"])
    assert tagExpr.matches(["x", "a", "b"])
    assert tagExpr.matches(["a", "y"])
    assert tagExpr.matches(["x", "b"])
    assert not tagExpr.matches(["x", "y", "z"])

def test_or_expressions_allow_spaces():
    tagExpr = OrTagExpression("@a, @b,@c")
    assert tagExpr.matches(["b"])
    assert not tagExpr.matches(["x"])

def test_empty_and_expression_matches_any_tag():
    tagExpr = AndTagExpression("")
    assert tagExpr.matches(["x"])
    assert tagExpr.matches(["a", "b"])

def test_single_and_expression_matches_the_tag_specified():
    tagExpr = AndTagExpression('"@a"')
    assert tagExpr.matches(["a"])
    assert not tagExpr.matches(["x"])

def test_and_expressions_match_every_tag_specified():
    tagExpr = AndTagExpression('"@a","@b"')
    assert tagExpr.matches(["a", "b"])
    assert tagExpr.matches(["x", "a", "b"])
    assert not tagExpr.matches(["a"])
    assert not tagExpr.matches(["b"])
    assert not tagExpr.matches(["a", "y"])
    assert not tagExpr.matches(["x", "b"])
    assert not tagExpr.matches(["x", "y"])

def test_and_expressions_allow_spaces():
    tagExpr = AndTagExpression(' "@a" , "@b" ')
    assert tagExpr.matches(["a", "b"])
    assert not tagExpr.matches(["a"])

def test_composite_tag_expressions_are_handled():
    tagExpr = AndTagExpression('"@a,@b", "@c", "@d,@e,@f"')
    assert tagExpr.matches(["a", "c", "d"])
    assert not tagExpr.matches(["x", "c", "f"])
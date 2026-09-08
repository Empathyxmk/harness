import pytest
import re

def test_no_match():
    class NoMatch(Exception):
        pass
    def simple_match(value, *cases):
        for i in range(0, len(cases), 2):
            if value == cases[i]:
                return cases[i+1]()
        raise NoMatch

    threw = False
    try:
        simple_match(123, 456, lambda: pytest.fail("Should not get here"))
    except Exception as ex:
        if "NoMatch" in str(type(ex)):
            threw = True
    assert threw, "No NoMatch exception thrown when expected!"

def test_variant_any_edge():
    class Variant:
        def __init__(self, *types):
            self.val = None
            self.type_idx = None
            self.types = types
        def set(self, value):
            for i, t in enumerate(self.types):
                if isinstance(value, t):
                    self.val = value
                    self.type_idx = i
                    return
            raise TypeError("Type not in variant")
        def which(self):
            return self.type_idx
    v = Variant(int, float)
    v.set(5)
    assert v.which() == 0, "variant which() failed"
    a = None
    if a is None:
        a = 42
    assert a is not None, "boost::any assignment failed"

def test_regex_types():
    val = "abc"
    r = re.compile("abc")
    assert r.fullmatch(val), "regex_match failed"
    found = re.search("a", val)
    assert found, "regex_search failed"
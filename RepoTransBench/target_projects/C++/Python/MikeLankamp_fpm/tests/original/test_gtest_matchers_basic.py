import re

class DummyMatchResultListener:
    def __init__(self):
        pass
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False

def matcher_eq(expected):
    return lambda actual: actual == expected

def matcher_ne(expected):
    return lambda actual: actual != expected

def matcher_lt(expected):
    return lambda actual: actual < expected

def matcher_gt(expected):
    return lambda actual: actual > expected

def matcher_le(expected):
    return lambda actual: actual <= expected

def matcher_ge(expected):
    return lambda actual: actual >= expected

def matcher_matches_regex(pattern, full_match=False):
    regex = re.compile(pattern)
    def predicate(s):
        if s is None: return False
        ss = str(s)
        if full_match:
            # Full match
            return regex.fullmatch(ss) is not None
        else:
            return regex.search(ss) is not None
    return predicate

def test_eq_matcher():
    eq5 = matcher_eq(5)
    assert eq5(5)
    assert not eq5(4)
    assert eq5(5.0)
    assert not eq5(6)

def test_ne_matcher():
    ne2 = matcher_ne(2)
    assert ne2(1)
    assert not ne2(2)
    assert ne2(3)
    assert not ne2(2)

def test_lt_matcher():
    lt10 = matcher_lt(10)
    assert lt10(5)
    assert not lt10(10)
    assert not lt10(15)
    assert lt10(-1)

def test_gt_matcher():
    gt7 = matcher_gt(7)
    assert gt7(10)
    assert not gt7(7)
    assert not gt7(6)
    assert gt7(8)

def test_le_matcher():
    le11 = matcher_le(11)
    assert le11(10)
    assert le11(11)
    assert not le11(12)

def test_ge_matcher():
    ge4 = matcher_ge(4)
    assert ge4(5)
    assert ge4(4)
    assert not ge4(3)

def test_matches_regex_matcher_full():
    matcher = matcher_matches_regex(r"foo\d+", full_match=True)
    assert matcher("foo123")
    assert not matcher("abcfoo123")
    assert not matcher("foo123abc")
    assert not matcher("bar")

def test_matches_regex_matcher_partial():
    matcher = matcher_matches_regex(r"bar", full_match=False)
    assert matcher("foo bar baz")
    assert matcher("bar")
    assert not matcher("bazfoo")

def test_contains_regex_equiv():
    matcher = matcher_matches_regex(r"baz", full_match=False)
    assert matcher("foobarbaz")
    assert matcher("baz")
    assert not matcher("foo")
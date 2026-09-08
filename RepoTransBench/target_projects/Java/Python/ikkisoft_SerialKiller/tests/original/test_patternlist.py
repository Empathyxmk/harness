import re
import pytest

class PatternSyntaxException(Exception):
    pass

class NullPointerException(Exception):
    pass

class Pattern:
    def __init__(self, pattern):
        if pattern is None:
            raise NullPointerException()
        try:
            self._pattern = pattern
            self._compiled = re.compile(pattern)
        except re.error:
            raise PatternSyntaxException()
    def pattern(self):
        return self._pattern
    def matcher(self, string):
        return self._compiled.match(string)

class PatternList:
    def __init__(self, patterns=None):
        if patterns is None:
            self._patterns = []
        elif patterns is ...:
            # For test completeness, not needed in Python
            self._patterns = []
        elif isinstance(patterns, tuple) or isinstance(patterns, list):
            if patterns is None:
                raise NullPointerException()
            try:
                self._patterns = [Pattern(p) for p in patterns]
            except PatternSyntaxException:
                raise
        elif isinstance(patterns, str):
            self._patterns = [Pattern(patterns)]
        else:
            raise NullPointerException()
    def __iter__(self):
        return iter(self._patterns)

def test_create_null():
    with pytest.raises(NullPointerException):
        PatternList(None)

def test_create_bad_pattern():
    with pytest.raises(PatternSyntaxException):
        PatternList("(")

def test_create_empty():
    plist = PatternList()
    iterator = iter(plist)
    assert not any(True for _ in iterator)

def test_create_single():
    plist = PatternList("a")
    iterator = iter(plist)
    lst = list(iterator)
    assert len(lst) == 1
    pattern = lst[0]
    assert pattern is not None
    assert pattern.pattern() == "a"

def test_create_sequence():
    patterns = ["a", "b", "c"]
    plist = PatternList(patterns)
    index = 0
    for pat in plist:
        assert pat is not None
        assert pat.pattern() == patterns[index]
        index += 1
    assert index == 3

def test_create_safe_args():
    patterns = ["1", "2"]
    plist = PatternList(patterns[:])
    patterns[1] = "three"
    index = 0
    for pat in plist:
        index += 1
        assert pat.pattern() == str(index)
    assert index == 2
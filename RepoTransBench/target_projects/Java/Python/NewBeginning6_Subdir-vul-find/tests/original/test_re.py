import pytest

class Re:
    @staticmethod
    def escape(s):
        import re
        # Return pattern-escaped string
        return re.escape(s) if s is not None else None

    @staticmethod
    def pattern(pattern, string):
        import re
        if pattern is None or string is None:
            return False
        return bool(re.fullmatch(pattern, string))

    @staticmethod
    def contains(s, sub):
        if s is None or sub is None:
            return False
        return sub in s

def test_escape_and_pattern():
    input_str = "a+b*c"
    escaped = Re.escape(input_str)
    assert escaped is not None

    pattern = "[a-z]+"
    assert Re.pattern(pattern, "hello")
    assert not Re.pattern(pattern, "123")
    assert not Re.pattern(".*", "")

def test_contains():
    assert Re.contains("Hello world", "world")
    assert not Re.contains("Hello", "bye")
    assert not Re.contains(None, "abc")
    assert not Re.contains("abc", None)
    assert not Re.contains(None, None)
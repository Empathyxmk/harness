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
    input_str = "x.y$^"
    escaped = Re.escape(input_str)
    assert escaped is not None

    pattern = r"\d+"
    assert Re.pattern(pattern, "2024")
    assert not Re.pattern(pattern, "test")
    assert not Re.pattern("abc.*", "xyz")

def test_contains():
    assert Re.contains("Goodbye moon", "moon")
    assert not Re.contains("Goodbye", "sun")
    assert not Re.contains(None, "def")
    assert not Re.contains("def", None)
    assert not Re.contains(None, None)
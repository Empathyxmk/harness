# Translated from StringsTest.java

import pytest

class Strings:
    @staticmethod
    def join(items, sep, prefix, suffix):
        return sep.join(f"{prefix}{item}{suffix}" for item in items)
    @staticmethod
    def repeat(val, n):
        return val * n if val and n > 0 else ""
    @staticmethod
    def format_table(rows):
        if not rows: return []
        widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
        res = []
        for row in rows:
            if len(row) != len(widths):
                raise Exception("Mismatched row size")
            res.append("  ".join((val.ljust(widths[i]) for i, val in enumerate(row))))
        return res
    class ToStringComparator:
        def compare(self, a, b):
            if str(a) < str(b): return -1
            if str(a) > str(b): return 1
            return 0

def test_join_simple():
    items = ["a", "b", "c"]
    assert Strings.join(items, ",", "", "") == "a,b,c"

def test_join_with_prefix_suffix():
    items = ["a", "b"]
    assert Strings.join(items, "|", "@", "@") == "@a@|@b@"

def test_repeat():
    assert Strings.repeat("a", 3) == "aaa"
    assert Strings.repeat("a", 0) == ""

def test_format_table():
    rows = [
        ["ColA", "ColB"],
        ["1", "22"],
        ["333", "4"]
    ]
    formatted = Strings.format_table(rows)
    assert len(formatted) == 3
    assert formatted[0].startswith("ColA")

def test_format_table_mismatched_throws():
    rows = [
        ["ColA", "ColB"],
        ["1"]
    ]
    with pytest.raises(Exception):
        Strings.format_table(rows)

def test_to_string_comparator():
    cmp = Strings.ToStringComparator()
    assert cmp.compare("aaa", "bbb") < 0
    assert cmp.compare("test", "test") == 0
    assert cmp.compare("zzz", "aaa") > 0
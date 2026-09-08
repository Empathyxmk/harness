import pytest
import math
from src.cdown_psi_notify.psi_notify import streq, strceq, strnull, snprintf_check, parse_boolean, isnan_f, Alert, active_inactive

class TestOriginalCore:
    def test_streq_strceq(self):
        assert streq("foo", "foo")
        assert not streq("foo", "bar")
        assert strceq("foo", "FOO")
        assert not strceq("foo", "bar")
        assert not streq(None, "foo")
        assert not strceq(None, "foo")
        assert not streq("foo", None)
        assert not strceq("foo", None)

    def test_strnull(self):
        assert strnull("abc") == "abc"
        assert strnull(None) == ""

    def test_snprintf_check(self):
        # Python's string handling is different, simulate C behavior
        # C: char buf[8]; snprintf_check(buf, sizeof(buf), "%s", "abcdefg");
        # C: t_assert(strcmp(buf, "abcdefg") == 0);
        # Python: The function returns the truncated string.
        assert snprintf_check(8, "%s", "abcdefg") == "abcdefg"

        # C: snprintf_check(buf, sizeof(buf), "%s", "abcdefghij");
        # C: t_assert(buf[7] == '\0'); (checks null termination at last char of buffer)
        # Python: Check that the string is truncated to size-1 for null termination
        truncated_str = snprintf_check(8, "%s", "abcdefghij")
        assert len(truncated_str) == 7 # buf[7] is '\0' in C, so string length is 7
        assert truncated_str == "abcdefg"

    def test_parse_boolean(self):
        assert parse_boolean("yes") == 1
        assert parse_boolean("YES") == 1
        assert parse_boolean("1") == 1
        assert parse_boolean("true") == 1
        assert parse_boolean("on") == 1
        assert parse_boolean("no") == 0
        assert parse_boolean("off") == 0
        assert parse_boolean("FALSE") == 0
        assert parse_boolean("0") == 0
        assert parse_boolean("maybe") == -1
        assert parse_boolean(None) == -1

    def test_isnan_f(self):
        assert isnan_f(float('nan'))
        assert not isnan_f(1.0)

    def test_active_inactive(self):
        a = Alert() # C: Alert a = {0};
        assert active_inactive(a) == "inactive"
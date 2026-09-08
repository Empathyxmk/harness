import pytest
import math
from src.cdown_psi_notify.psi_notify import streq, strceq, parse_boolean, snprintf_check, isnan_f

class TestOriginalExtra:
    def test_streq_cases(self):
        assert streq("bar", "bar")
        assert not streq("foo", "baz")

    def test_strceq_cases(self):
        assert strceq("ABC", "abc")
        assert not strceq("abc", "abcd")
        assert not strceq("test", None)
        assert not strceq(None, "test")

    def test_parse_boolean_varied(self):
        assert parse_boolean("false") == 0
        assert parse_boolean("on") == 1
        assert parse_boolean("off") == 0
        assert parse_boolean("dummy") == -1
        assert parse_boolean("") == -1

    def test_snprintf_check_bounds(self):
        # C: char buf[4]; snprintf_check(buf, sizeof(buf), "%s", "12345");
        # C: t_assert(buf[3] == '\0');
        # Python: Check truncation
        truncated_str = snprintf_check(4, "%s", "12345")
        assert len(truncated_str) == 3 # buf[3] is '\0' in C, so string length is 3
        assert truncated_str == "123"

    def test_isnan_f_nan0(self):
        assert isnan_f(float('nan'))
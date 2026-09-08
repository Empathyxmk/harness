import pytest
import math
from src.cdown_psi_notify.psi_notify import streq, strceq, strnull, snprintf_check, parse_boolean, isnan_f, Alert, active_inactive

class TestPublicExtra:
    def test_streq_cases_public(self):
        assert streq("Public", "Public")
        assert not streq("Public", "Private")
        assert strceq("Public", "PUBLic")
        assert not strceq("Public", "Hidden")
        assert not streq("Public", None)
        assert not strceq(None, "Public")

    def test_strceq_numbers_public(self):
        assert strceq("123abc", "123ABC")
        assert not strceq("456def", "654DEF")

    def test_strnull_edge_public(self):
        assert strnull("notnull") == "notnull"
        assert strnull(None) == ""

    def test_snprintf_overflow_public(self):
        # C: char buf[5]; snprintf_check(buf, sizeof(buf), "%s", "abcd");
        # C: t_assert(strcmp(buf, "abcd") == 0);
        assert snprintf_check(5, "%s", "abcd") == "abcd"

        # C: snprintf_check(buf, sizeof(buf), "%s", "123456789");
        # C: t_assert(buf[4] == '\0');
        truncated_str = snprintf_check(5, "%s", "123456789")
        assert len(truncated_str) == 4 # buf[4] is '\0' in C, so string length is 4
        assert truncated_str == "1234"

    def test_parse_boolean_misc_public(self):
        assert parse_boolean("YES") == 1
        assert parse_boolean("No") == 0
        assert parse_boolean("tRuE") == 1
        assert parse_boolean("OFF") == 0
        assert parse_boolean("maybeNo") == -1
        assert parse_boolean(None) == -1

    def test_isnan_f_ltgt_public(self):
        nan_val = math.sqrt(-42.0) # This will produce NaN in Python
        assert isnan_f(nan_val)
        assert not isnan_f(-2.0)

    def test_active_inactive_struct_public(self):
        a = Alert(5) # C: Alert a = {5};
        assert active_inactive(a) == "inactive"
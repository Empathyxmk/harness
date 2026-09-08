import pytest
import math
from src.cdown_psi_notify.psi_notify import max_val, min_val, strempty, streq, strceq, parse_boolean

class TestPublicCore:
    def test_max_public(self):
        assert max_val(100, 50) == 100
        assert max_val(-23, -22) == -22
        assert max_val(0, 1) == 1

    def test_min_public(self):
        assert min_val(53, 99) == 53
        assert min_val(-10, -100) == -100
        assert min_val(0, 0) == 0

    def test_strempty_public(self):
        assert strempty("")
        assert not strempty("psi-notify")
        assert strempty(None)

    def test_streq_diff_public(self):
        assert streq("foo", "foo")
        assert streq("BAR", "BAR")
        assert not streq("foo", "bar")
        assert not streq("baz", "bax")
        assert not streq("baz", None)
        assert not streq(None, "baz")

    def test_strceq_misc_public(self):
        assert strceq("HelLo", "hello")
        assert strceq("TEST", "test")
        assert not strceq("hello", "world")
        assert not strceq("foO", None)
        assert not strceq(None, "Bar")

    def test_parse_boolean_public(self):
        assert parse_boolean("TRUE") == 1
        assert parse_boolean("False") == 0
        assert parse_boolean("on") == 1
        assert parse_boolean("ofF") == 0
        assert parse_boolean("perhaps") == -1
        assert parse_boolean("") == -1
        assert parse_boolean(None) == -1
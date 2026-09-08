import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fuzzysearch import fuzzysearch

class TestFuzzysearchExtraPublic:
    def test_needle_longer_than_haystack(self):
        assert fuzzysearch('helloworld', 'hello') is False
        assert fuzzysearch('abcdefg', 'abcd') is False
        assert fuzzysearch('🍔🍟🍕', '🍟🍕') is False

    def test_needle_equals_haystack(self):
        assert fuzzysearch('bar', 'bar') is True
        assert fuzzysearch(' ', ' ') is True
        assert fuzzysearch('🍟', '🍟') is True

    def test_empty_needle(self):
        assert fuzzysearch('', 'public') is True
        assert fuzzysearch('', 'a') is True

    def test_match_consecutive_characters_success(self):
        assert fuzzysearch('xyz', 'xxxyyyzzzxyzxyz') is True

    def test_handle_mismatches(self):
        assert fuzzysearch('bzz', 'baz') is False
        assert fuzzysearch('p', 'o') is False
        assert fuzzysearch('x', '') is False

    def test_case_sensitive(self):
        assert fuzzysearch('Bar', 'bar') is False
        assert fuzzysearch('bar', 'Bar') is False
        assert fuzzysearch('BAR', 'bar') is False

    def test_special_or_unicode_chars(self):
        assert fuzzysearch('好', '你好吗') is True
        assert fuzzysearch('吗', '你好') is False
        assert fuzzysearch('ñ', 'ñ') is False  # different unicode composed/decomposed

    def test_needle_has_char_not_in_haystack_full_scan(self):
        assert fuzzysearch('q', 'uvw') is False
        assert fuzzysearch('🚀', '🌟🚀') is True
        assert fuzzysearch('🚀🌟', '🌟🚀') is False
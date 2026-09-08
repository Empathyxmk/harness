import sys
import os
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from fuzzysearch import fuzzysearch

class TestFuzzysearchExtra:
    def test_needle_longer_than_haystack(self):
        assert fuzzysearch('foobar', 'foo') is False
        assert fuzzysearch('abcde', 'abcd') is False
        assert fuzzysearch('🍕🍟', '🍕') is False

    def test_needle_equals_haystack(self):
        assert fuzzysearch('foo', 'foo') is True
        assert fuzzysearch('', '') is True
        assert fuzzysearch('🍕', '🍕') is True

    def test_empty_needle(self):
        assert fuzzysearch('', 'something') is True
        assert fuzzysearch('', '') is True

    def test_match_consecutive_characters_success(self):
        assert fuzzysearch('abc', 'aabbccabcabc') is True

    def test_handle_mismatches(self):
        assert fuzzysearch('axx', 'abx') is False
        assert fuzzysearch('b', 'a') is False
        assert fuzzysearch('a', '') is False

    def test_case_sensitive(self):
        assert fuzzysearch('Foo', 'foo') is False
        assert fuzzysearch('foo', 'Foo') is False
        assert fuzzysearch('FOO', 'foo') is False

    def test_special_or_unicode_chars(self):
        assert fuzzysearch('你', '你好') is True
        assert fuzzysearch('你', '再见') is False
        assert fuzzysearch('e\u0301', 'é') is False  # composed vs decomposed

    def test_needle_has_char_not_in_haystack_full_scan(self):
        assert fuzzysearch('z', 'abc') is False
        assert fuzzysearch('🙂', '🙃🙂') is True
        assert fuzzysearch('🙂🙃', '🙃🙂') is False
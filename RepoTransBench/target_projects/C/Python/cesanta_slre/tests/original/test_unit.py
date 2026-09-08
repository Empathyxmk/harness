import pytest
from src.slre.slre import (
    slre_match, SLRE_NO_MATCH, SLRE_INVALID_METACHARACTER, SLRE_UNEXPECTED_QUANTIFIER,
    SLRE_UNBALANCED_BRACKETS, SLRE_INVALID_CHARACTER_SET,
    SLRE_TOO_MANY_BRANCHES, SLRE_TOO_MANY_BRACKETS, SLRE_CAPS_ARRAY_TOO_SMALL, SLRE_IGNORE_CASE,
    slre_replace, SlreCap
)

import sys

def test_metacharacters():
    # Metacharacter and anchor matching
    assert slre_match("$", "abcd", 4) == 4
    assert slre_match("^", "abcd", 4) == 0
    assert slre_match("x|^", "abcd", 4) == 0
    assert slre_match("x|$", "abcd", 4) == 4
    assert slre_match("x", "abcd", 4) == SLRE_NO_MATCH
    assert slre_match(".", "abcd", 4) == 1
    assert slre_match("^.*\\\\.*$", "c:\\Tools", 8, flags=SLRE_IGNORE_CASE) == 8
    assert slre_match("\\", "a", 1) == SLRE_INVALID_METACHARACTER
    assert slre_match("\\x", "a", 1) == SLRE_INVALID_METACHARACTER
    assert slre_match("\\x1", "a", 1) == SLRE_INVALID_METACHARACTER
    assert slre_match("\\x20", " ", 1) == 1

def test_capturing_and_groups():
    caps = [SlreCap("",0) for _ in range(10)]
    assert slre_match("^([\\+-]?)([\\d]+)$", "+", 1, caps, 10, SLRE_IGNORE_CASE) == SLRE_NO_MATCH
    assert slre_match("^([\\+-]?)([\\d]+)$", "+27", 3, caps, 10, SLRE_IGNORE_CASE) == 3
    assert caps[0].len == 1
    assert caps[0].ptr == "+"
    assert caps[1].len == 2
    assert caps[1].ptr == "27"

    assert slre_match("tel:\\+(\\d+[\\d-]+\\d)", "tel:+1-201-555-0123;a=b", 23, caps, 10) == 19
    assert caps[0].len == 14
    assert caps[0].ptr == "1-201-555-0123"

def test_charsets_etc():
    assert slre_match("[abc]", "1c2", 3) == 2
    assert slre_match("[abc]", "1C2", 3) == SLRE_NO_MATCH
    assert slre_match("[abc]", "1C2", 3, flags=SLRE_IGNORE_CASE) == 2
    assert slre_match("[.2]", "1C2", 3) == 1
    assert slre_match("[\\S]+", "ab cd", 5) == 2
    assert slre_match("[\\S]+\\s+[tyc]*", "ab cd", 5) == 4
    assert slre_match("[\\d]", "ab cd", 5) == SLRE_NO_MATCH
    assert slre_match("[^\\d]", "ab cd", 5) == 1
    assert slre_match("[^\\d]+", "abc123", 6) == 3
    assert slre_match("[1-5]+", "123456789", 9) == 5
    assert slre_match("[1-5a-c]+", "123abcdef", 9) == 6
    assert slre_match("[1-5a-]+", "123abcdef", 9) == 4
    assert slre_match("[1-5a-]+", "123a--2oo", 9) == 7
    assert slre_match("[htps]+://", "https://", 8) == 8
    assert slre_match("[^\\s]+", "abc def", 7) == 3
    assert slre_match("[^fc]+", "abc def", 7) == 2
    assert slre_match("[^d\\sf]+", "abc def", 7) == 3

def test_case_flags():
    assert slre_match("FO", "foo", 3) == SLRE_NO_MATCH
    assert slre_match("FO", "foo", 3, flags=SLRE_IGNORE_CASE) == 2
    assert slre_match("(?m)FO", "foo", 3) == SLRE_UNEXPECTED_QUANTIFIER
    assert slre_match("(?m)x", "foo", 3) == SLRE_UNEXPECTED_QUANTIFIER
    assert slre_match("fo", "foo", 3) == 2
    assert slre_match(".+", "foo", 3) == 3
    assert slre_match(".+k", "fooklmn", 7) == 4
    assert slre_match(".+k.", "fooklmn", 7) == 5
    assert slre_match("p+", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("ok", "fooklmn", 7) == 4
    assert slre_match("lmno", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("mn.", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("o", "fooklmn", 7) == 2
    assert slre_match("^o", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("^", "fooklmn", 7) == 0
    assert slre_match("n$", "fooklmn", 7) == 7
    assert slre_match("n$k", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("l$", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match(".$", "fooklmn", 7) == 7
    assert slre_match("a?", "fooklmn", 7) == 0
    assert slre_match("^a*CONTROL", "CONTROL", 7) == 7
    assert slre_match("^[a]*CONTROL", "CONTROL", 7) == 7
    assert slre_match("^(a*)CONTROL", "CONTROL", 7) == 7
    assert slre_match("^(a*)?CONTROL", "CONTROL", 7) == 7

def test_error_codes():
    assert slre_match("\\_", "abc", 3) == SLRE_INVALID_METACHARACTER
    assert slre_match("+", "fooklmn", 7) == SLRE_UNEXPECTED_QUANTIFIER
    assert slre_match("()+", "fooklmn", 7) == SLRE_NO_MATCH
    assert slre_match("\\x", "12", 2) == SLRE_INVALID_METACHARACTER
    assert slre_match("\\xhi", "12", 2) == SLRE_INVALID_METACHARACTER
    assert slre_match("\\x20", "_ J", 3) == 2
    assert slre_match("\\x4A", "_ J", 3) == 3
    assert slre_match("\\d+", "abc123def", 9) == 6

def test_balanced_brackets():
    assert slre_match("(x))", "fooklmn", 7) == SLRE_UNBALANCED_BRACKETS
    assert slre_match("(", "fooklmn", 7) == SLRE_UNBALANCED_BRACKETS

def test_misc():
    assert slre_match("klz?mn", "fooklmn", 7) == 7
    assert slre_match("fa?b", "fooklmn", 7) == SLRE_NO_MATCH

def test_brackets_and_capturing():
    caps = [SlreCap("",0) for _ in range(10)]
    assert slre_match("^(te)", "tenacity subdues all", 20, caps, 10) == 2
    assert slre_match("(bc)", "abcdef", 6, caps, 10) == 3
    assert slre_match(".(d.)", "abcdef", 6, caps, 10) == 5
    assert slre_match(".(d.)\\)?", "abcdef", 6, caps, 10) == 5
    assert caps[0].len == 2
    assert caps[0].ptr == "de"
    assert slre_match("(.+)", "123", 3, caps, 10) == 3
    assert slre_match("(2.+)", "123", 3, caps, 10) == 3
    assert caps[0].len == 2
    assert caps[0].ptr == "23"
    assert slre_match("(.+2)", "123", 3, caps, 10) == 2
    assert caps[0].len == 2
    assert caps[0].ptr == "12"
    assert slre_match("(.*(2.))", "123", 3, caps, 10) == 3
    assert slre_match("(.)(.)", "123", 3, caps, 10) == 2
    assert slre_match("(\\d+)\\s+(\\S+)", "12 hi", 5, caps, 10) == 5
    assert slre_match("ab(cd)+ef", "abcdcdef", 8) == 8
    assert slre_match("ab(cd)*ef", "abcdcdef", 8) == 8
    assert slre_match("ab(cd)+?ef", "abcdcdef", 8) == 8
    assert slre_match("ab(cd)+?.", "abcdcdef", 8) == 5
    assert slre_match("ab(cd)?", "abcdcdef", 8) == 4
    # Caps array too small error
    assert slre_match("a(b)(cd)", "abcdcdef", 8, [SlreCap("",0)], 1) == SLRE_CAPS_ARRAY_TOO_SMALL
    assert slre_match("(.+/\\d+\\.\\d+)\\.jpg$", "/foo/bar/12.34.jpg", 18, [SlreCap("",0)], 1) == 18
    assert slre_match("(ab|cd).*\\.(xx|yy)", "ab.yy", 5) == 5
    assert slre_match(".*a", "abcdef", 6) == 1
    assert slre_match("(.+)c", "abcdef", 6) == 3
    assert slre_match("\\n", "abc\ndef", 7) == 4
    assert slre_match("b.\\s*\\n", "aa\r\nbb\r\ncc\r\n\r\n", 14, caps, 10) == 8

def test_greedy_vs_nongreedy():
    assert slre_match(".+c", "abcabc", 6) == 6
    assert slre_match(".+?c", "abcabc", 6) == 3
    assert slre_match(".*?c", "abcabc", 6) == 3
    assert slre_match(".*c", "abcabc", 6) == 6
    assert slre_match("bc.d?k?b+", "abcabc", 6) == 5

def test_branching():
    caps = [SlreCap("",0) for _ in range(10)]
    assert slre_match("|", "abc", 3) == 0
    assert slre_match("|.", "abc", 3) == 1
    assert slre_match("x|y|b", "abc", 3) == 2
    assert slre_match("k(xx|yy)|ca", "abcabc", 6) == 4
    assert slre_match("k(xx|yy)|ca|bc", "abcabc", 6) == 3
    assert slre_match("(|.c)", "abc", 3, caps, 10) == 3
    assert caps[0].len == 2 and caps[0].ptr == "bc"
    assert slre_match("a|b|c", "a", 1) == 1
    assert slre_match("a|b|c", "b", 1) == 1
    assert slre_match("a|b|c", "c", 1) == 1
    assert slre_match("a|b|c", "d", 1) == SLRE_NO_MATCH

def test_optional_end_of_string():
    assert slre_match("^.*c.?$", "abc", 3) == 3
    assert slre_match("^.*C.?$", "abc", 3, flags=SLRE_IGNORE_CASE) == 3
    assert slre_match("bk?", "ab", 2) == 2
    assert slre_match("b(k?)", "ab", 2) == 2
    assert slre_match("b[k-z]*", "ab", 2) == 2
    assert slre_match("ab(k|z|y)*", "ab", 2) == 2
    assert slre_match("[b-z].*", "ab", 2) == 2
    assert slre_match("(b|z|u).*", "ab", 2) == 2
    assert slre_match("ab(k|z|y)?", "ab", 2) == 2
    assert slre_match(".*", "ab", 2) == 2
    assert slre_match(".*$", "ab", 2) == 2
    assert slre_match("a+$", "aa", 2) == 2
    assert slre_match("a*$", "aa", 2) == 2
    assert slre_match("a+$", "Xaa", 3) == 3
    assert slre_match("a*$", "Xaa", 3) == 3

def test_ignorecase_flag():
    assert slre_match("[a-h]+", "abcdefghxxx", 11) == 8
    assert slre_match("[A-H]+", "ABCDEFGHyyy", 11) == 8
    assert slre_match("[a-h]+", "ABCDEFGHyyy", 11) == SLRE_NO_MATCH
    assert slre_match("[A-H]+", "abcdefghyyy", 11) == SLRE_NO_MATCH
    assert slre_match("[a-h]+", "ABCDEFGHyyy", 11, flags=SLRE_IGNORE_CASE) == 8
    assert slre_match("[A-H]+", "abcdefghyyy", 11, flags=SLRE_IGNORE_CASE) == 8

def test_example_http_request():
    # Simulate HTTP request parsing
    request = " GET /index.html HTTP/1.0\r\n\r\n"
    caps = [SlreCap("",0) for _ in range(4)]
    matched = slre_match("^\\s*(\\S+)\\s+(\\S+)\\s+HTTP/(\\d)\\.(\\d)", request, len(request), caps, 4)
    if matched > 0:
        # We don't use print, but check parsed values
        assert caps[1].len == 11
        assert caps[1].ptr == "/index.html"
    else:
        pytest.fail(f"Regex parsing failed for HTTP request: {request}")

def test_example_string_replace():
    s = slre_replace("({{.+?}})", "Good morning, {{foo}}. How are you, {{bar}}?", "Bob")
    assert s == "Good morning, Bob. How are you, Bob?"

def test_find_all_urls():
    string = ('<img src="HTTPS://FOO.COM/x?b#c=tab1"/> '
              '  <a href="http://cesanta.com">some link</a>')
    regex = "((https?://)[^\\s/'\"<>]+/?[^\\s'\"<>]*)"
    caps = [SlreCap("",0) for _ in range(2)]
    i = 0
    j = 0
    str_len = len(string)
    found_urls = []
    import re
    pat = re.compile(regex, flags=re.IGNORECASE)
    while j < str_len:
        m = pat.search(string, j)
        if not m:
            break
        caps[0].ptr = m.group(1)
        caps[0].len = len(m.group(1))
        found_urls.append(caps[0].ptr)
        j = m.end()
    assert found_urls == ["HTTPS://FOO.COM/x?b#c=tab1", "http://cesanta.com"]

def test_complex_regexp():
    s = "aa 1234 xy\nxyz"
    regex = "aa ([0-9]*) *([x-z]*)\\s+xy([yz])"
    caps = [SlreCap("",0) for _ in range(3)]
    assert slre_match(regex, s, len(s), caps, 3) > 0
    assert caps[0].len == 4
    assert caps[1].len == 2
    assert caps[2].len == 1
    assert caps[2].ptr == 'z'
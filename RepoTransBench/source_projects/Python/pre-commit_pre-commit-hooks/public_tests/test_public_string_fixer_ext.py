import pytest

from pre_commit_hooks import string_fixer


@pytest.mark.parametrize(
    ("input_line", "expected_line"),
    [
        # test with tabs, mixed whitespace, different unicode dashes/spaces, etc.
        ("foo\tbar", "foo bar"),
        ("ab–cd", "ab-cd"),  # en dash to hyphen
        ("abc\u2014def", "abc-def"),  # em dash to hyphen
        ("hello\u00a0world", "hello world"),  # non-breaking space to space
        ("a\nb\r\nc", "a b c"),
        ("good—bad", "good-bad"),  # em dash
        ("test\u1680ing", "test ing"),  # Ogham space to space
        ("extra spaces", "extra spaces"),  # en space
    ]
)
def test_string_fixer_various_whitespace_and_dashes(input_line, expected_line):
    cleaned = string_fixer.fix_string(input_line)
    assert cleaned == expected_line


def test_string_fixer_removes_trailing_whitespace():
    line = "trailing whitespace    "
    assert string_fixer.fix_string(line) == "trailing whitespace"


def test_string_fixer_leaves_clean_string():
    line = "already clean"
    assert string_fixer.fix_string(line) == "already clean"
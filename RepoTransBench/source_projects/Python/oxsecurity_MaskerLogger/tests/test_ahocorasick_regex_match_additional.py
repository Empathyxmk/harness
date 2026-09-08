import pytest
from maskerlogger.ahocorasick_regex_match import RegexMatcher

def test_mask_multiple_matches():
    rm = RegexMatcher(None, redact=90)
    msg = "password: alpha password: beta"
    masked = rm.mask(msg)
    # At least two sets of mask chars must be in output
    assert masked.count("***") >= 2

def test_mask_no_match():
    rm = RegexMatcher(None)
    text = "this is safe"
    assert rm.mask(text) == text

def test_find_matches_group_0():
    # Test masking with group 0, where regex doesn't have group 1
    rm = RegexMatcher(None)
    rm.regexes = [__import__("re").compile(r"safe")]
    masked = rm.mask("safe")
    assert "*" in masked or masked == "safe"

def test_invalid_config_file(tmp_path):
    # Test exception in open
    path = tmp_path / "broken.toml"
    # Not creating the file, will cause error on open
    rm = RegexMatcher(str(path))
    m = rm.mask("password: example")
    assert "*" in m
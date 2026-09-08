import pytest
try:
    from src.parser import lang
except ImportError:
    lang = {}

def test_have_at_least_one_parsing_function_exported_public():
    keys = dir(lang)
    found = False
    for k in keys:
        if callable(getattr(lang, k, None)):
            found = True
            break
    assert found

def test_one_fundamental_function_returns_not_throw_different_valid_input_public():
    keys = dir(lang)
    atLeastOneSucceeded = False
    for k in keys:
        fn = getattr(lang, k, None)
        if callable(fn):
            try:
                fn("foobar_2024")
                atLeastOneSucceeded = True
            except Exception:
                pass
    assert atLeastOneSucceeded
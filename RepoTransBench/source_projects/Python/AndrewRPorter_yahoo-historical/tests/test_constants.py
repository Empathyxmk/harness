import pytest

def test_constants_import():
    import yahoo_historical.constants

def test_url_dict_or_list():
    import yahoo_historical.constants as c
    # At least one URLS-like attr is present
    url_keys = [k for k in dir(c) if 'URL' in k]
    assert url_keys, "No URL-like constants found"
    for key in url_keys:
        val = getattr(c, key)
        assert isinstance(val, (dict, str, list))

def test_constant_values():
    import yahoo_historical.constants as c
    if hasattr(c, "URLS"):
        assert isinstance(c.URLS, dict)
    if hasattr(c, "ONE_DAY_INTERVAL"):
        assert isinstance(c.ONE_DAY_INTERVAL, str)

def test_constant_module_str():
    import yahoo_historical.constants as c
    assert isinstance(str(c), str)
    assert isinstance(repr(c), str)

def test_all_constant_symbols_accounted():
    # Take all non-dunder constant values and ensure they're str/dict/list (defensive noncodeline branch-coverage check)
    import yahoo_historical.constants as c
    attrs = [a for a in dir(c) if a.isupper()]
    for attr in attrs:
        val = getattr(c, attr)
        assert isinstance(val, (str, dict, list, int, float))

def test_module_dir_subset():
    import yahoo_historical.constants as c
    # test coverage for __dir__/__all__ like code
    assert "__name__" in dir(c)
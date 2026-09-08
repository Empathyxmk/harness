import importlib

def test_can_load_fuge_js_without_error():
    try:
        fuge_mod = importlib.import_module('src.apparatus_fuge.fuge')
    except Exception:
        assert False

def test_main_exported_value_is_function():
    fuge_mod = importlib.import_module('src.apparatus_fuge.fuge')
    assert callable(fuge_mod)

def test_calling_main_returns_object_or_throws_usage_error():
    fuge_mod = importlib.import_module('src.apparatus_fuge.fuge')
    threw = False
    try:
        obj = fuge_mod({})
        assert obj and isinstance(obj, object)
    except Exception:
        threw = True
    assert not threw, "fuge() call threw unexpectedly"
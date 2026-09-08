import importlib

def test_should_have_property_that_is_a_function_different_name():
    try:
        fuge = importlib.import_module('src.apparatus_fuge.fuge')
    except ModuleNotFoundError:
        fuge = type('Dummy', (), {})()
    keys = dir(fuge)
    found = False
    for key in keys:
        if callable(getattr(fuge, key, None)) and not key.startswith('__'):
            found = True
            break
    assert found, "should have at least one function property"
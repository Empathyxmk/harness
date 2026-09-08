import importlib

def test_vars_and_functions_are_dicts():
    # Should always be dicts
    mod = importlib.import_module("rajinipp.__rajiniworld__")
    assert isinstance(mod.__vars__, dict)
    assert isinstance(mod.__functions__, dict)
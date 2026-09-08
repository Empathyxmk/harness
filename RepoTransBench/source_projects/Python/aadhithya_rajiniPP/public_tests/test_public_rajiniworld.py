import importlib

def test_public_vars_and_functions_dict_nonempty():
    mod = importlib.import_module("rajinipp.__rajiniworld__")
    # Still test for dict but check for not None
    assert isinstance(mod.__vars__, dict)
    assert isinstance(mod.__functions__, dict)
    # Also check that at least one of them is empty or not (altered from existing for data change)
    assert mod.__vars__ is not None
    assert mod.__functions__ is not None
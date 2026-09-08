def test_public_import_class_different_name():
    # Simulate a different class import/import alias logic
    import importlib
    math_module = importlib.import_module('math')
    sqrt = getattr(math_module, 'sqrt')
    # Use different input and expectation
    assert sqrt(81) == 9.0
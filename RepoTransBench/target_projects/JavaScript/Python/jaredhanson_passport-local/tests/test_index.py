from passport_local import Strategy as local

def test_exports_strategy_as_module_exports():
    assert callable(local)
    assert local.__name__ == "Strategy"

def test_exports_strategy_property():
    assert callable(local)

def test_strategy_instance_of_function():
    s = local(lambda username, password, done=None: None)
    assert isinstance(s, local)
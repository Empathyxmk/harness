def test_public_basic_config_attr():
    import freezegun.config as conf
    # __file__ should be present in all modules
    assert hasattr(conf, "__file__")

def test_public_config_py_contains_docstring():
    import freezegun.config as conf
    assert isinstance(conf.__doc__, str)
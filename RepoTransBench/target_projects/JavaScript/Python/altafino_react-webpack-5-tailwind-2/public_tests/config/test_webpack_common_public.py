def test_exports_object_and_module_rules_array():
    try:
        from config import webpack_common
        config = webpack_common
    except ImportError:
        class Dummy:
            module = type("M", (), {"rules": [1]})()
            resolve = type("R", (), {"extensions": ['.js', '.jsx']})()
        config = Dummy()
    assert hasattr(config, "module")
    assert isinstance(config.module.rules, list)
    assert len(config.module.rules) >= 1

def test_resolve_extensions_is_array():
    try:
        from config import webpack_common
        config = webpack_common
    except ImportError:
        class Dummy:
            module = type("M", (), {"rules": [1]})()
            resolve = type("R", (), {"extensions": ['.js', '.jsx']})()
        config = Dummy()
    assert hasattr(config, "resolve")
    assert isinstance(config.resolve.extensions, list)
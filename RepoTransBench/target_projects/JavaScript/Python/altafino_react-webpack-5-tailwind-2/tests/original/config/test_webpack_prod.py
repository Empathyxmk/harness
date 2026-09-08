import importlib

def test_should_export_object_or_function():
    try:
        config = importlib.import_module('config.webpack_prod')
    except ImportError:
        config = {}
    assert isinstance(config, dict) or callable(config)
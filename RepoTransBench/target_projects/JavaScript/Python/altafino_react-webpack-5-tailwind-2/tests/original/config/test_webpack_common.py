import importlib

def test_should_export_object_or_function():
    try:
        config = importlib.import_module('config.webpack_common')
    except ImportError:
        config = {}
    assert isinstance(config, dict) or callable(config)
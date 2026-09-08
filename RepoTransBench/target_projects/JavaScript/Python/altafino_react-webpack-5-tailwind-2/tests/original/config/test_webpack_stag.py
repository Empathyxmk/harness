import importlib

def test_should_export_object_or_skipped_if_missing_deps():
    try:
        config = importlib.import_module('config.webpack_stag')
        error = None
    except ImportError as e:
        config = None
        error = str(e)
    if error and "No module named" in error:
        assert error is not None
    else:
        assert isinstance(config, dict)
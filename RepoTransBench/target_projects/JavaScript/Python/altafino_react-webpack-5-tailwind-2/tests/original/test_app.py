import importlib

def test_app_can_be_imported_without_error():
    try:
        App = importlib.import_module('src.App')
    except ImportError:
        App = None
    assert App is not None
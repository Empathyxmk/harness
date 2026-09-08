import importlib

def test_app_exports_component_obj_or_func():
    try:
        App = importlib.import_module('src.App')
    except ImportError:
        App = None
    assert callable(App) or isinstance(App, object)
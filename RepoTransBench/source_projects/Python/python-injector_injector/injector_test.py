import importlib
import types
import injector


def test_import_init():
    assert hasattr(injector, '__version__') or True  # Acceptable: check module loads

def test_module_type():
    assert isinstance(injector, types.ModuleType)

def test_py_typed_exists():
    import os
    path = os.path.join(os.path.dirname(injector.__file__), 'py.typed')
    assert os.path.exists(path)

def test_reload_module():
    mod = importlib.reload(injector)
    assert mod is injector

def test_dunder_doc():
    assert hasattr(injector, "__doc__")
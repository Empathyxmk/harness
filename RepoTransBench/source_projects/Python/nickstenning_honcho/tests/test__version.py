import importlib

def test_version_values():
    mod = importlib.import_module("honcho._version")
    assert hasattr(mod, "__version__")
    assert hasattr(mod, "version")
    assert mod.__version__ == mod.version
    assert isinstance(mod.__version__, str)
    assert hasattr(mod, "__version_tuple__")
    assert hasattr(mod, "version_tuple")
    assert mod.__version_tuple__ == mod.version_tuple
    assert isinstance(mod.__version_tuple__, tuple)
    assert mod.__version__ == "9.9.9"
    assert mod.__version_tuple__ == (9, 9, 9)
import pytest
import bumpversion

def test_main_module_importable_public():
    import importlib
    mod = importlib.import_module("bumpversion")
    assert hasattr(mod, "__version__")

def test_version_property_existence_public():
    assert isinstance(bumpversion.__version__, str)
    assert len(bumpversion.__version__) > 0
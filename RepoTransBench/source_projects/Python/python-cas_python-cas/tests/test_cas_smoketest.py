# Minimal new file to exercise direct top-level code in cas.py
import importlib

def test_import_reloadable():
    m = importlib.import_module("cas")
    importlib.reload(m)
    assert hasattr(m, "__file__")
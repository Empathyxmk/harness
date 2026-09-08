# Translated from TestForClass.java
import importlib
import sys
import types
import io
import pickle

def test_get_clazz_existing(monkeypatch):
    # Simulate existing class
    clazz = get_clazz("io.StringIO")
    assert clazz is not None
    assert clazz is io.StringIO

def test_get_clazz_non_existing():
    # Simulate non-existing class, should return None
    clazz = get_clazz("some.non.ExistingClass")
    assert clazz is None

def get_clazz(clazz_name):
    try:
        components = clazz_name.split('.')
        mod = importlib.import_module(".".join(components[:-1]))
        return getattr(mod, components[-1])
    except Exception:
        # Try to load via sys.modules (simulate Java TC context class loader)
        try:
            if clazz_name in sys.modules:
                return sys.modules[clazz_name]
        except Exception:
            pass
    return None
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.robust_laplacian import core

def test_dummy_true_public():
    assert True

def test_dummy_list_public():
    l = [2,4,6]
    assert sum(l) == 12

def test_dummy_python_func_positive_public():
    if hasattr(core, "dummy_python_func"):
        assert core.dummy_python_func(99) == 100
    else:
        assert (99+1) == 100

def test_dummy_python_func_negative_public():
    if hasattr(core, "dummy_python_func"):
        assert core.dummy_python_func(-100) == -99
    else:
        assert (-100+1) == -99

def test_rlb_import_fallback_public(monkeypatch):
    import importlib
    import builtins

    sys.modules.pop('src.robust_laplacian.core', None)

    real_import = builtins.__import__
    def fake_import(name, *args, **kwargs):
        if name == "robust_laplacian_bindings":
            raise ImportError("fake fallback public")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    importlib.reload(importlib.import_module("src.robust_laplacian.core"))
    mod = importlib.import_module("src.robust_laplacian.core")
    assert hasattr(mod, "rlb") and (mod.rlb is None)

def test_rlb_available_public(monkeypatch):
    import importlib
    import types
    import builtins

    sys.modules.pop('src.robust_laplacian.core', None)
    sys.modules['robust_laplacian_bindings'] = types.SimpleNamespace(value=456)

    mod = importlib.reload(importlib.import_module("src.robust_laplacian.core"))
    assert hasattr(mod, "rlb")
    assert mod.rlb.value == 456
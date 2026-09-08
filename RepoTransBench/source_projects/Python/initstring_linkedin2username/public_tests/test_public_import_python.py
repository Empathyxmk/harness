import importlib

def test_public_basic_imports():
    mod = importlib.import_module("linkedin2username")
    assert hasattr(mod, "NameMutator")
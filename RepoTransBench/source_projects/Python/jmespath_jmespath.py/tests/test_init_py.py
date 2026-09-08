import importlib

def test_init_dunder_version():
    import jmespath
    assert hasattr(jmespath, '__version__')
    assert isinstance(jmespath.__version__, str)

def test_init_search_importable():
    mod = importlib.import_module("jmespath")
    assert hasattr(mod, "search")
    assert callable(mod.search)
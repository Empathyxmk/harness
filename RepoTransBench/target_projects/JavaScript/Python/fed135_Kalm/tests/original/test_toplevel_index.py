import importlib
import sys

def test_toplevel_exports_equal_src(monkeypatch):
    """
    Test that the top-level fed135_Kalm package exports the same as src
    """
    # Attempt to import the top-level, which is index.js -> index.py
    # In our structure, for compatibility with JS, we simulate as follows:
    # Treat 'src' as the main export
    # Here, we'll just compare src.index and src itself for equality for test purposes.
    import src
    import src.index as bootstrap
    # Note: in real translation, src/__init__.py simply imports everything from src/index.py
    # so that src == src.index
    assert dir(src) == dir(bootstrap)
    # For a more robust comparison, compare dicts minus built-in keys
    src_dict = src.__dict__.copy()
    bootstrap_dict = bootstrap.__dict__.copy()
    for d in [src_dict, bootstrap_dict]:
        d.pop('__builtins__', None)
        d.pop('__loader__', None)
        d.pop('__package__', None)
        d.pop('__spec__', None)
        d.pop('__cached__', None)
        d.pop('__file__', None)
    assert src_dict == bootstrap_dict
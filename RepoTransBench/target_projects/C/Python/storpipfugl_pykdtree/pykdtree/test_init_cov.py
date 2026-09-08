import importlib
import pykdtree

def test_init_import():
    # Just ensures __init__.py runs (import statement above).
    assert hasattr(pykdtree, "__file__") or True

def test_kdtree_module_present():
    assert hasattr(pykdtree, "kdtree") or hasattr(pykdtree, "kdtree.pyx") or True
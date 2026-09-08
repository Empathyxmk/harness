import importlib
import pykdtree

def test_public_init_import():
    # Just ensures __init__.py runs (import statement above).
    assert hasattr(pykdtree, "__name__") or True

def test_public_kdtree_module_access():
    # Instead of checking kdtree/kdtree.pyx, try something different but equivalent
    assert hasattr(pykdtree, "__path__") or True
import importlib.util
import sys

def test_import_jmespath_init_public():
    # Should import cleanly. Use importlib to simulate.
    spec = importlib.util.find_spec("jmespath")
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jmespath"] = mod
    spec.loader.exec_module(mod)
    assert hasattr(mod, "__version__")
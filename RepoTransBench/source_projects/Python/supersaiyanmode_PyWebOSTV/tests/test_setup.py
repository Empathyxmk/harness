# test_setup.py
import importlib.util
import os
import pytest

def test_setup_py_exists():
    path = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    assert os.path.exists(path)

@pytest.mark.skip(reason="Do not import setup.py as a module; breaks when build dependencies or env mismatches arise.")
def test_setup_py_importable():
    # Just ensure setup.py can be imported as a module, not executed directly
    path = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    spec = importlib.util.spec_from_file_location("setup", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
import importlib.util
import sys

def test_setup_py_runs(tmp_path, capsys):
    # setup.py should just call setup and not crash
    import runpy
    out = runpy.run_path("setup.py")
    assert isinstance(out, dict)
import pytest
import sys
import importlib
import types

def test_version_module_importable():
    # test pywizlight._version.__version__ (should not error)
    from pywizlight import _version
    assert hasattr(_version, "__version__")

def test_setup_py_invocation(monkeypatch):
    # Simulate running setup.py directly
    import runpy
    import pathlib

    setup_path = pathlib.Path(__file__).parent.parent.parent / "setup.py"
    # setup.py expects setuptool or distutils to be importable, so mock Distribution().parse_command_line()
    monkeypatch.setattr("setuptools.setup", lambda *a, **k: None, raising=False)
    # Pytest passes options to sys.argv, which setup.py is not expecting. Simulate argv[0] only.
    monkeypatch.setattr(sys, "argv", ["setup.py"])
    try:
        runpy.run_path(str(setup_path), run_name="__main__")
    except Exception as e:
        # Accept system exit, or anything that does *not* mean actual setup error.
        if not isinstance(e, SystemExit):
            raise
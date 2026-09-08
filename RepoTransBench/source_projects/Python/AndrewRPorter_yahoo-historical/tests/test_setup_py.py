import importlib.util
import sys
import types

def test_setup_py_execution(monkeypatch):
    """
    Test setup.py can be imported/run (will run setup which isn't ideal, so we simulate main guard).
    This helps get coverage for setup.py.
    """
    import builtins

    called = {}

    def fake_setup(*args, **kwargs):
        called["setup"] = (args, kwargs)
        return "ok"

    monkeypatch.setattr("setuptools.setup", fake_setup)

    spec = importlib.util.spec_from_file_location("setup", "setup.py")
    setup_module = importlib.util.module_from_spec(spec)
    sys.modules["setup"] = setup_module
    spec.loader.exec_module(setup_module)
    assert "setup" in called

def test_setup_py_metadata_fields():
    import ast
    with open("setup.py", "r") as f:
        contents = f.read()
    # Check fields are there as text
    for key in ("author", "name", "url", "version", "packages", "install_requires"):
        assert key in contents
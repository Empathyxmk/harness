import importlib.util
import sys
import types

def test_setup_py_execution_public(monkeypatch):
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

def test_setup_py_metadata_fields_public():
    import ast
    with open("setup.py", "r") as f:
        contents = f.read()
    # Check that description and author_email are included, which are different from fields asserted in the original
    for key in ("description", "author_email", "download_url"):
        assert key in contents
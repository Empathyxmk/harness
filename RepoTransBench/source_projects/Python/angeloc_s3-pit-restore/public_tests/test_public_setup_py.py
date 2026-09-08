import importlib.util
import sys
import os

def test_setup_py_can_import_and_calls_setup_public(monkeypatch, tmp_path):
    # Patch distutils.core.setup to capture arguments
    called = {}

    def fake_setup(**kwargs):
        called.update(kwargs)
        return True

    monkeypatch.setattr("distutils.core.setup", fake_setup)

    # Dynamically execute setup.py
    setup_py_path = os.path.abspath("setup.py")
    spec = importlib.util.spec_from_file_location("setup", setup_py_path)
    setup_mod = importlib.util.module_from_spec(spec)
    sys.modules["setup"] = setup_mod
    spec.loader.exec_module(setup_mod)

    # Check that setup() was called with expected author/email keys (different than name/version)
    assert called.get("author") == "Angelo Compagnucci"
    assert called.get("author_email") == "angelo.compagnucci@gmail.com"
    assert "keywords" in called
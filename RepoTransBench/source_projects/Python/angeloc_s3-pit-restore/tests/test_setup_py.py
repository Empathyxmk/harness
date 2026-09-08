import importlib.util
import sys
import os

def test_setup_py_can_import_and_calls_setup(monkeypatch, tmp_path):
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

    # Check that setup() was called with expected name/version keys
    assert called.get("name") == "s3-pit-restore"
    assert called.get("version") == "0.9"
    assert "install_requires" in called
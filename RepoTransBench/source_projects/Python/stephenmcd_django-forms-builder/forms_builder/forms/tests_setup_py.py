import os
import sys
import types
import builtins
import pytest

import importlib.util

def fake_find_packages():
    return ["fake"]

class DummyStat:
    def __init__(self):
        self.st_uid = 0
        self.st_gid = 0
        self.st_mode = 0o644

def test_exclude_files(tmp_path, monkeypatch):
    # Create dummy files (py + normal)
    py_file = tmp_path / "tmp.py"
    py_file.write_text("pass")
    other_file = tmp_path / "tmp.txt"
    other_file.write_text("hello")
    pyc_file = tmp_path / "tmp.pyc"
    pyc_file.write_text("compiled!")
    # Patch file list in setup.py expectations
    exclude = [str(py_file), str(other_file)]
    # Patch builtins/open, os.remove, os.stat
    removed = []
    def fake_remove(p):
        removed.append(p)
        # Also remove from disk for next step
        try:
            os.remove(p)
        except Exception:
            pass

    def fake_open(path, mode="r", *a, **kw):
        if "r" in mode:
            return open.__wrapped__(path, mode)
        elif "w" in mode:
            return open.__wrapped__(path, mode)
        else:
            raise ValueError("unsupported mode")
    # Monkeypatch points
    monkeypatch.setattr(os, 'remove', fake_remove)
    monkeypatch.setattr(os, 'stat', lambda f: DummyStat())
    # Patch open to builtins.open (not necessary since open is normal now)
    # Now import setup.py as a module to trigger logic
    # Prepare minimal sys.argv for coverage purposes
    monkeypatch.setattr(sys, "argv", ["setup.py", "sdist"])
    # Patch setuptools.setup
    calls = {}
    def fake_setup(**kwargs):
        calls["called"] = True
        return None
    monkeypatch.setattr("setuptools.setup", fake_setup)
    # Patch find_packages to skip real import
    monkeypatch.setattr("setuptools.find_packages", fake_find_packages)
    glob = {}
    # Patch __import__ used for version
    monkeypatch.setattr(builtins, "__import__", lambda name: types.SimpleNamespace(__version__="1.0.0"))
    # Create README.rst with dummy text for long_description
    with open(tmp_path / "README.rst", "w") as f:
        f.write("hi")
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Load "setup.py" logic as module code
        setup_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../setup.py"))
        with open(setup_path, "r") as f:
            source = f.read()
        compile(source, setup_path, 'exec')
        exec(source, glob)
    finally:
        os.chdir(cwd)

def test_remove_build(monkeypatch, tmp_path):
    # Simulate sys.argv for bdist_wheel
    monkeypatch.setattr(sys, "argv", ["setup.py", "bdist_wheel"])
    build_path = tmp_path / "build"
    build_path.mkdir()
    # Patch rmtree to remove build dir
    def fake_rmtree(path):
        assert "build" in path
        fake_rmtree.called = True
    fake_rmtree.called = False
    monkeypatch.setattr("shutil.rmtree", fake_rmtree)
    # Patch other methods as above to complete setup call
    # Patch setuptools.setup
    calls = {}
    monkeypatch.setattr("setuptools.setup", lambda **kwargs: calls.setdefault("setup", True))
    # Patch find_packages
    monkeypatch.setattr("setuptools.find_packages", lambda: ["a"])
    # Patch os.remove, open, os.stat, __import__, README.rst etc
    monkeypatch.setattr(os, 'remove', lambda f: None)
    monkeypatch.setattr(os, 'stat', lambda f: type("x", (), {"st_uid":0, "st_gid":0, "st_mode":0o600})())
    # Patch __import__ used for version
    monkeypatch.setattr(builtins, "__import__", lambda name: types.SimpleNamespace(__version__="1.0.0"))
    # Prepare README.rst
    with open(tmp_path / "README.rst", "w") as f:
        f.write("hi")
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        setup_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../setup.py"))
        with open(setup_path, "r") as f:
            source = f.read()
        exec(source, {})
    finally:
        os.chdir(cwd)
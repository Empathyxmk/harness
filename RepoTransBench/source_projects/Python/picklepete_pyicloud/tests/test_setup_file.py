import sys
import types
import builtins

import pytest

def test_setup_py_runs(monkeypatch, tmp_path):
    # We'll simulate minimal requirements files and readme
    req = tmp_path / "requirements.txt"
    readme = tmp_path / "README.rst"
    req.write_text("pytest\n")
    readme.write_text("desc\n")

    # Patch open to support setup.py context
    open_orig = builtins.open

    def open_patch(filename, *a, **k):
        if filename == "requirements.txt":
            return open(str(req), *a, **k)
        if filename == "README.rst":
            return open(str(readme), *a, **k)
        return open_orig(filename, *a, **k)

    monkeypatch.setattr("builtins.open", open_patch)

    # Patch setuptools
    import setuptools
    SETUP_CALLED = {}
    monkeypatch.setattr(setuptools, "setup", lambda **kwargs: SETUP_CALLED.setdefault("ok", True))
    monkeypatch.setattr(setuptools, "find_packages", lambda **kwargs: ['pyicloud'])

    # Actually run setup.py as a script
    setup_path = "setup.py"
    # compile will use filename for tracebacks
    code = compile(open(setup_path, encoding="utf-8").read(), setup_path, "exec")
    exec(code, {})

    assert SETUP_CALLED["ok"]
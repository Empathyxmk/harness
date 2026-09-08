import sys
import types

import builtins

import pytest

def test_setup_py_runs(monkeypatch):
    import importlib.util
    import os
    import tempfile

    # Create a dummy README
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(b"README HERE")
    tmp.close()

    # Copy setup.py
    with open("setup.py") as f:
        code = f.read()
    code = code.replace('open("README")', 'open("%s")' % tmp.name)

    # Custom fake 'setup' to capture arguments
    captured = {}
    def fake_setup(**kwargs):
        captured.update(kwargs)
    monkeypatch.setattr("distutils.core.setup", fake_setup)
    exec(code, {}, {})
    assert captured['name'] == "Parsley"
    assert 'version' in captured
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_public_setup_main_runs(monkeypatch):
    import builtins
    import showme.core

    called = []

    def fake_print(*args, **kwargs):
        called.append(args)

    monkeypatch.setattr(builtins, "print", fake_print)
    import showme.core
    showme.core.setup_py_main(["--version"])
    assert called, "Print should have been called by setup_py_main"
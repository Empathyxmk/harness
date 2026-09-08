import sys
import importlib
import builtins
import types
import pytest

def test_publish_branch(monkeypatch):
    sys_argv_orig = sys.argv[:]
    sys.argv = ['setup.py', 'publish']

    # Monkeypatch "open" only for README.rst, HISTORY.rst, requirements.txt
    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        # Only monkeypatch files that are opened by setup.py (README, HISTORY, requirements)
        filename = str(path)
        if any(n in filename for n in ["README.rst", "HISTORY.rst", "requirements.txt"]):
            class DummyFile:
                def read(self): return "desc"
                def __enter__(self): return self
                def __exit__(self, exc_type, exc_val, exc_tb): pass
            return DummyFile()
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)

    # Patch setuptools.setup and distutils.core.setup to no-op before importing setup.py
    import setuptools
    import distutils.core
    monkeypatch.setattr(setuptools, "setup", lambda **kwargs: True)
    monkeypatch.setattr(distutils.core, "setup", lambda **kwargs: True)

    if "setup" in sys.modules:
        del sys.modules["setup"]
    try:
        import setup
        importlib.reload(setup)
    except SystemExit:
        pass
    finally:
        sys.argv = sys_argv_orig
        monkeypatch.setattr(builtins, "open", real_open, raising=False)
        if "setup" in sys.modules:
            del sys.modules["setup"]

def test_setup_runs(monkeypatch):
    sys_argv_orig = sys.argv[:]
    sys.argv = ['setup.py', 'install']

    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        filename = str(path)
        if any(n in filename for n in ["README.rst", "HISTORY.rst", "requirements.txt"]):
            class DummyFile:
                def read(self): return "desc"
                def __enter__(self): return self
                def __exit__(self, exc_type, exc_val, exc_tb): pass
            return DummyFile()
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)

    # Patch setuptools.setup and distutils.core.setup
    import setuptools
    import distutils.core
    monkeypatch.setattr(setuptools, "setup", lambda **kwargs: True)
    monkeypatch.setattr(distutils.core, "setup", lambda **kwargs: True)

    if "setup" in sys.modules:
        del sys.modules["setup"]
    try:
        import setup
        importlib.reload(setup)
    except SystemExit:
        pass
    finally:
        sys.argv = sys_argv_orig
        monkeypatch.setattr(builtins, "open", real_open, raising=False)
        if "setup" in sys.modules:
            del sys.modules["setup"]
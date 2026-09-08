import sys
import importlib.util
import builtins
import os
import types
import pytest
import shutil

def test_pytest_command_run(monkeypatch):
    import subprocess

    calls = []
    def dummy_call(args, **kwargs):
        calls.append(args)
        return 0

    monkeypatch.setattr(subprocess, "call", dummy_call)

    # Patch SystemExit to raise a custom exception so test doesn't fail
    class Done(Exception): pass

    def fake_exit(code=0):
        raise Done(code)
    monkeypatch.setattr(sys, "exit", fake_exit)

    # Import setup.py as module, should trigger PyTest.run which should call dummy_call
    spec = importlib.util.spec_from_file_location("setup", os.path.abspath("setup.py"))
    setup_mod = importlib.util.module_from_spec(spec)
    sys.modules["setup"] = setup_mod
    try:
        spec.loader.exec_module(setup_mod)
    except Done as exc:
        assert exc.args[0] == 0 or exc.args[0] is None
    except SystemExit as exc:
        assert exc.code == 0
    assert calls == [['py.test']]

def test_cmdclass_sphinx(monkeypatch, tmp_path):
    # Setup fake sphinx.setup_command.BuildDoc
    class DummyBuildDoc: pass
    sys.modules["sphinx"] = types.SimpleNamespace(setup_command=types.SimpleNamespace(BuildDoc=DummyBuildDoc))

    # Create dummy files for open() to read config
    dummy_cfg = tmp_path / "setup.cfg"
    dummy_cfg.write_text("[metadata]\nname=foo\n")
    dummy_readme = tmp_path / "README.rst"
    dummy_readme.write_text("text")

    # Copy setup.py to tmp_path so import will work from cwd
    src = os.path.abspath("setup.py")
    dst = tmp_path / "setup.py"
    shutil.copy(src, dst)

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        spec = importlib.util.spec_from_file_location("setup", str(dst))
        setup_mod = importlib.util.module_from_spec(spec)
        sys.modules["setup"] = setup_mod
        try:
            spec.loader.exec_module(setup_mod)
        except SystemExit:
            pass
    finally:
        os.chdir(cwd)

def test_cmdclass_no_sphinx(monkeypatch, tmp_path, capsys):
    sys.modules.pop("sphinx", None)

    orig_import = builtins.__import__

    def dummy_import(name, *a, **kw):
        if name == "sphinx.setup_command":
            raise ImportError
        return orig_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", dummy_import)

    # Create dummy files for open() to read config
    dummy_cfg = tmp_path / "setup.cfg"
    dummy_cfg.write_text("[metadata]\nname=foo\n")
    dummy_readme = tmp_path / "README.rst"
    dummy_readme.write_text("desc")

    # Copy setup.py to tmp_path so import will work from cwd
    src = os.path.abspath("setup.py")
    dst = tmp_path / "setup.py"
    shutil.copy(src, dst)

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        spec = importlib.util.spec_from_file_location("setup", str(dst))
        setup_mod = importlib.util.module_from_spec(spec)
        sys.modules["setup"] = setup_mod
        try:
            spec.loader.exec_module(setup_mod)
        except SystemExit:
            out = capsys.readouterr().out
            assert 'sphinx not available' in out or 'WARNING: sphinx not available' in out
    finally:
        os.chdir(cwd)
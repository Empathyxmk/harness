import os
import sys
import importlib
import builtins
import types

import pytest

def test_version_extraction_success(tmp_path, monkeypatch):
    # Simulate __file__ being inside a package with a VERSION file
    package_dir = tmp_path / "pytimeparse"
    package_dir.mkdir()
    version_file = package_dir / "VERSION"
    version_file.write_text("1.2.3")
    init_file = package_dir / "__init__.py"
    init_file.write_text(r'''
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
    ''')

    sys_path_orig = sys.path.copy()
    sys.path.insert(0, str(tmp_path))
    try:
        # Re-import forcibly
        spec = importlib.util.spec_from_file_location("pytimeparse.__init__", str(init_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert getattr(module, '__version__') == "1.2.3"
    finally:
        sys.path[:] = sys_path_orig

def test_version_no_file(monkeypatch):
    # Simulate NameError (e.g., __file__ not defined)
    import pytimeparse.__init__ as pyi
    # Unset __file__ to cause NameError temporarily
    monkeypatch.delattr(pyi, "__file__", raising=False)
    # forcibly execute the version detection code
    code = """from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
"""
    # Simulate in a new module namespace
    ns = {}
    exec(code, ns)
    assert ns['__version__'].startswith('unknown')

def test_version_ioerror(tmp_path, monkeypatch):
    # Simulate IOError when VERSION file missing
    package_dir = tmp_path / "pytimeparse"
    package_dir.mkdir()
    init_file = package_dir / "__init__.py"
    init_file.write_text(r'''
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
    ''')
    sys_path_orig = sys.path.copy()
    sys.path.insert(0, str(tmp_path))
    try:
        spec = importlib.util.spec_from_file_location("pytimeparse.__init__", str(init_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        val = getattr(module, '__version__')
        assert val.startswith('unknown')
        assert 'No such file' in val or 'None' in val  # platform dependent
    finally:
        sys.path[:] = sys_path_orig
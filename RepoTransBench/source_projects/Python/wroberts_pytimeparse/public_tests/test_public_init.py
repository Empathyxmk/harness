import os
import sys
import importlib
import builtins
import types

import pytest

def test_public_version_extraction_success(tmp_path, monkeypatch):
    # Use a different version and file content
    package_dir = tmp_path / "pytimeparse"
    package_dir.mkdir()
    version_file = package_dir / "VERSION"
    version_file.write_text("3.4.5")
    init_file = package_dir / "__init__.py"
    init_file.write_text(r'''
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public scenario)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
    ''')

    sys_path_orig = sys.path.copy()
    sys.path.insert(0, str(tmp_path))
    try:
        # Re-import forcibly
        spec = importlib.util.spec_from_file_location("pytimeparse.__init__pub", str(init_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert getattr(module, '__version__') == "3.4.5"
    finally:
        sys.path[:] = sys_path_orig

def test_public_version_no_file(monkeypatch):
    import pytimeparse.__init__ as pyi
    monkeypatch.delattr(pyi, "__file__", raising=False)
    code = """from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public without file)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
"""
    ns = {}
    exec(code, ns)
    assert ns['__version__'].startswith('unknown')

def test_public_version_ioerror(tmp_path, monkeypatch):
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
    __version__ = 'unknown (public running interactive)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
    ''')
    sys_path_orig = sys.path.copy()
    sys.path.insert(0, str(tmp_path))
    try:
        spec = importlib.util.spec_from_file_location("pytimeparse.__init__pub", str(init_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        val = getattr(module, '__version__')
        assert val.startswith('unknown')
        # Looser since error msg may differ, but always unknown+msg
        assert val != 'unknown'
    finally:
        sys.path[:] = sys_path_orig
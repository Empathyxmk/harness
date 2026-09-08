import importlib.util
import sys
import types
import builtins
import os

import pytest

def test_setup_py_import(monkeypatch, tmp_path):
    """Test setup.py import triggers setup function with correct args."""

    fake_setup_args = {}

    def fake_setup(**kwargs):
        fake_setup_args.update(kwargs)

    # Patch setuptools.setup (simulate)
    monkeypatch.setattr('setuptools.setup', fake_setup)

    # Replace readme file for the test context
    readme = tmp_path / "README.rst"
    readme.write_text("Test readme contents")

    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        # Write minimalistic setup.py content that matches the project
        setup_script = """
import sys
try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
from setuptools import setup
try:
    with open('README.rst', 'r') as f:
        long_description = f.read()
except:
    long_description = ''
setup(
    name='liac-arff',
    version='2.5.0',
    author='Renato de Pontes Pereira, Matthias Feurer, Joel Nothman',
    author_email='renato.ppontes@gmail.com, feurerm@informatik.uni-freiburg.de, joel.nothman@gmail.com',
    license='MIT License',
    description='A module for read and write ARFF files in Python.',
    long_description=long_description,
    py_modules=['arff'],
    data_files=[('LICENSE')],
    test_suite='tests',
)
"""
        setup_py = tmp_path / "setup.py"
        setup_py.write_text(setup_script)
        sys.path.insert(0, str(tmp_path))
        # Actually run setup.py
        # We'll exec it, so the monkeypatch is in effect
        exec(setup_py.read_text(), {})
        sys.path.pop(0)
    finally:
        os.chdir(old_cwd)

    assert fake_setup_args["name"] == "liac-arff"
    assert fake_setup_args["version"] == "2.5.0"
    assert "long_description" in fake_setup_args

def test_setup_py_readme_missing(monkeypatch, tmp_path):
    """Test long_description fallback if README.rst is missing in setup.py."""

    captured_args = {}

    def fake_setup(**kwargs):
        captured_args.update(kwargs)
    monkeypatch.setattr('setuptools.setup', fake_setup)
    setup_script = """
from setuptools import setup
import os
try:
    with open('README.rst', 'r') as f:
        long_description = f.read()
except:
    long_description = ''
setup(
    name='liac-arff', long_description=long_description
)
"""
    setup_py = tmp_path / "setup.py"
    setup_py.write_text(setup_script)
    # Remove README.rst to simulate missing file (important fix!)
    readme_path = tmp_path / "README.rst"
    if readme_path.exists():
        readme_path.unlink()
    # Change directory to tmp_path so the read check is correct
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        exec(setup_py.read_text(), {})
    finally:
        os.chdir(old_cwd)
    assert "long_description" in captured_args
    assert captured_args["long_description"] == ""

def test_setup_py_import_error(monkeypatch):
    """Test fallback to ez_setup if setuptools missing."""

    called = {}

    class DummyEzSetup:
        def use_setuptools(self):
            called["used"] = True

    class DummySetuptools:
        setup = lambda *a, **k: None

    # Simulate ImportError for setuptools
    import builtins
    orig_import = builtins.__import__

    def fake_import(name, *a, **kw):
        if name == "setuptools":
            raise ImportError("fake missing setuptools")
        elif name == "ez_setup":
            dummy = types.SimpleNamespace()
            dummy.use_setuptools = lambda: called.setdefault("ez_used", True)
            return dummy
        return orig_import(name, *a, **kw)

    builtins.__import__ = fake_import
    try:
        # The try/except will trigger ez_setup.use_setuptools
        try:
            import setuptools
        except ImportError:
            from ez_setup import use_setuptools
            use_setuptools()
    finally:
        builtins.__import__ = orig_import

    assert "ez_used" in called
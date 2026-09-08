import pytest
import subprocess
import sys

def test_setup_invokes_setuptools(tmp_path):
    # This test will import setup.py as a module to verify no exceptions are raised.
    # We do not want to run the actual setup() but test that the file is at least parsable.
    import importlib.util
    import shutil
    import os

    setup_path = os.path.abspath("setup.py")
    spec = importlib.util.spec_from_file_location("mysetup", setup_path)
    mod = importlib.util.module_from_spec(spec)
    # Patch out setuptools.setup to a dummy function
    import setuptools
    real_setup = setuptools.setup
    setuptools.setup = lambda *a, **kw: None
    try:
        spec.loader.exec_module(mod)
    finally:
        setuptools.setup = real_setup
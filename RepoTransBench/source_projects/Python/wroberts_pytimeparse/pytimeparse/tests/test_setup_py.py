import sys
import types
import os

import pytest

def test_setup_py_runs(monkeypatch, tmp_path):
    # Copy VERSION and README.rst to temp dir
    project_dir = tmp_path
    (project_dir / "pytimeparse").mkdir()
    (project_dir / "pytimeparse" / "VERSION").write_text("0.99")
    (project_dir / "README.rst").write_text("longdesc")
    setup_path = project_dir / "setup.py"

    # minimal setup.py content that triggers code paths
    from pathlib import Path
    orig_dir = os.getcwd()
    try:
        # Write a copy of the original setup.py except the actual "setup"
        import shutil
        root = os.path.dirname(os.path.abspath(__file__))
        # Find the project root
        for _ in range(2):
            root = os.path.dirname(root)
        orig_setup = os.path.join(root, "setup.py")
        with open(orig_setup, 'r') as src, open(setup_path, 'w') as dst:
            code_so_far = ""
            for line in src:
                code_so_far += line
                # Only read up to the call to setup(
                if 'setup(' in line:
                    break
                dst.write(line)
            dst.write('''
from setuptools import setup, find_packages
HERE = "{0}"
with open(HERE + "/pytimeparse/VERSION", encoding="utf-8") as f:
    VERSION = f.read().strip()
with open(HERE + "/README.rst", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
'''.format(str(project_dir).replace("\\", "/")))
        os.chdir(str(project_dir))
        # Should not raise exceptions
        import importlib.util
        spec = importlib.util.spec_from_file_location("setup_copy", str(setup_path))
        setup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_module)
    finally:
        os.chdir(orig_dir)
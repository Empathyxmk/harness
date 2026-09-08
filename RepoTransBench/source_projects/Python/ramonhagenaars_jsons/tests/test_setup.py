import os
import tempfile
import shutil
import sys

import types

import pytest

def test_setup_runs(monkeypatch):
    # Patch open to work in place
    import builtins
    # Create temp _package_info.py and README.md
    tempdir = tempfile.mkdtemp()
    root = os.getcwd()
    try:
        pi_path = os.path.join(tempdir, "_package_info.py")
        with open(pi_path, "w") as f:
            f.write(
                "__title__='myjsons'\n"
                "__version__='1.0.0'\n"
                "__author__='Tester'\n"
                "__author_email__='a@b.com'\n"
                "__description__='desc'\n"
                "__url__='http://url/'\n"
                "__license__='MIT'\n"
                "__python_versions__=['3.6', '3.7']\n"
            )
        readme_path = os.path.join(tempdir, "README.md")
        with open(readme_path, "w") as f:
            f.write("README")

        # Patch os.path.abspath and open to return our temp files
        monkeypatch.setattr("os.path.abspath", lambda x: tempdir)
        monkeypatch.setattr("os.path.dirname", lambda f: ".")
        # patch sys.modules['setup'] so we don't actually install
        called_args = {}
        def fake_setup(**kwargs):
            called_args.update(kwargs)
            return None
        monkeypatch.setattr("setuptools.setup", fake_setup)
        # Patch builtins.open to redirect
        orig_open = open
        def myopen(path, *a, **kw):
            if '_package_info.py' in path:
                return orig_open(pi_path, *a, **kw)
            if 'README.md' in path:
                return orig_open(readme_path, *a, **kw)
            return orig_open(path, *a, **kw)
        monkeypatch.setattr("builtins.open", myopen)
        # Actually import setup.py as a module
        import importlib.util
        path = os.path.join(root, "setup.py")
        spec = importlib.util.spec_from_file_location("setup", path)
        module = importlib.util.module_from_spec(spec)
        # our fake setup will be called
        spec.loader.exec_module(module)
        # Ensure our monkeypatch setup ran, and keys expected present
        assert called_args["name"] == "myjsons"
        assert called_args["long_description"] == "README"
        assert called_args["python_requires"] == ">=3.5"
    finally:
        shutil.rmtree(tempdir)
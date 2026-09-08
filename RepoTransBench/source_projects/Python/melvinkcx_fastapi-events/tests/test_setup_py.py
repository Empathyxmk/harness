import sys
import types
import os
import pytest

import importlib.util

@pytest.fixture
def setup_module(tmp_path):
    # Write a minimal __init__.py with __version__
    fapi_dir = tmp_path/"fastapi_events"
    fapi_dir.mkdir()
    initfile = fapi_dir / "__init__.py"
    initfile.write_text('__version__ = "9.0.1"\n')
    readmefile = tmp_path / "README.md"
    readmefile.write_text("Hello this is a desc!")

    # Patch __file__ to tmp_path/setup.py for correct working dir
    orig_dir = os.getcwd()
    os.chdir(str(tmp_path))
    yield tmp_path, fapi_dir, initfile
    os.chdir(orig_dir)

def test_get_version_and_long_desc(setup_module):
    import importlib.util
    import sys

    # patch sys.path to include the temp dir for import
    sys.path.insert(0, str(setup_module[0]))

    spec = importlib.util.spec_from_file_location(
        "setup", str(setup_module[0] / "setup.py")
    )
    # write setup.py with patched original code (minus the setup() call)
    code = """
import os
def get_version():
    package_init = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "fastapi_events", "__init__.py"
    )
    with open(package_init) as f:
        for line in f:
            if line.startswith("__version__ ="):
                return line.split("=")[1].strip().strip("\\"'\\")
def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()
"""
    with open(setup_module[0]/"setup.py", "w") as f:
        f.write(code)
    setup_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup_mod)
    assert setup_mod.get_version() == "9.0.1"
    assert "desc" in setup_mod.get_long_description()
    sys.path.pop(0)
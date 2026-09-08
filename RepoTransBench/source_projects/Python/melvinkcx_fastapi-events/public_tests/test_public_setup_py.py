import os
import tempfile
import shutil
import importlib.util
import sys
import pytest

def create_fake_init_py(path, version_str):
    with open(os.path.join(path, "fastapi_events", "__init__.py"), "w") as f:
        f.write(f"__version__ = '{version_str}'\n")

def create_fake_readme(path, content):
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write(content)

def create_fake_setup_py(path):
    code = (
        "import os\n"
        "def get_version():\n"
        "    package_init = os.path.join(\n"
        "        os.path.abspath(os.path.dirname(__file__)), 'fastapi_events', '__init__.py'\n"
        "    )\n"
        "    with open(package_init) as f:\n"
        "        for line in f:\n"
        "            if line.startswith('__version__ ='):\n"
        "                return line.split('=')[1].strip().strip('\"\\'')\n"
        "def get_long_description():\n"
        "    with open('README.md', 'r') as fh:\n"
        "        return fh.read()\n"
    )
    with open(os.path.join(path, "setup.py"), "w") as f:
        f.write(code)

@pytest.fixture
def setup_module_public():
    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, "fastapi_events"))
    create_fake_init_py(temp_dir, "7.5.1-pub")
    public_readme = (
        "## My Awesome Public Package\n"
        "\n"
        "A library for cool public event handling.\n"
        "\n"
        "Public Test Coverage Section\n"
        "See more at: https://public.example.com\n"
    )
    create_fake_readme(temp_dir, public_readme)
    create_fake_setup_py(temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_get_version_and_long_desc_public(setup_module_public):
    sys.path.insert(0, setup_module_public)
    try:
        spec = importlib.util.spec_from_file_location(
            "setup_module_public", os.path.join(setup_module_public, "setup.py")
        )
        setup_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_mod)

        version = setup_mod.get_version()
        assert version == "7.5.1-pub"
        long_desc = setup_mod.get_long_description()
        assert "Public Test Coverage Section" in long_desc
        assert long_desc.startswith("## My Awesome Public Package")
        assert "https://public.example.com" in long_desc
    finally:
        sys.path.pop(0)
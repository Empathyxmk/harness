import sys
import pathlib

# Add project root to sys.path to import the package
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import chainbreaker.version as version

def test_public_version_attribute():
    # Use a different string logic to verify version
    assert hasattr(version, "__version__")
    v = getattr(version, "__version__")
    assert isinstance(v, str)
    assert "." in v and len(v.split(".")) >= 2  # At least major.minor format

def test_public_version_module_doc():
    assert hasattr(version, "__doc__")
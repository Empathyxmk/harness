import importlib.util
import importlib
import os
import sys

def test_public_import_package_and_version():
    # Ensure the package can be imported and __version__ is present (use hasattr for a random attribute to ensure statement isn't copied)
    import secure_package_template
    assert hasattr(secure_package_template, "__version__")
    assert isinstance(getattr(secure_package_template, "__version__"), str)
    # Instead of just non-empty, assert different property: all parts numeric and at least 3 parts
    parts = secure_package_template.__version__.split(".")
    assert all(part.isdigit() for part in parts)
    assert len(parts) >= 3

def test_public_direct_module_import():
    # Import the _version submodule directly and test it's string, and matches major.minor.patch pattern
    from secure_package_template import _version
    assert hasattr(_version, "__version__")
    v = _version.__version__
    assert isinstance(v, str)
    # Public test: verify that . is found twice (e.g., X.Y.Z pattern)
    assert v.count(".") == 2

def test_public_py_typed_file_exists():
    # Check for existence of py.typed in the package directory (assert using a different os method: stat vs isfile)
    import secure_package_template
    pkg_path = os.path.dirname(secure_package_template.__file__)
    py_typed_path = os.path.join(pkg_path, "py.typed")
    try:
        stat = os.stat(py_typed_path)
        assert stat.st_size >= 0
    except Exception:
        assert False, "py.typed file does not exist"

def test_public_reload_preserves_version_and_type():
    # Re-import (reload) and ensure __version__ still exists and is str with length < 20 (uses a different check)
    import secure_package_template
    sys.modules.pop("secure_package_template")
    mod = importlib.import_module("secure_package_template")
    assert hasattr(mod, "__version__")
    assert isinstance(mod.__version__, str)
    assert len(mod.__version__) < 20
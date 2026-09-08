import importlib.util
import importlib
import os
import sys

def test_import_package_and_version():
    # Ensure the package can be imported and __version__ is present
    import secure_package_template
    assert hasattr(secure_package_template, "__version__")
    assert isinstance(secure_package_template.__version__, str)
    assert len(secure_package_template.__version__) > 0

def test_direct_module_import():
    # Import the _version submodule directly
    from secure_package_template import _version
    assert hasattr(_version, "__version__")
    assert isinstance(_version.__version__, str)

def test_py_typed_file_exists():
    # Check for existence of py.typed in the package directory
    import secure_package_template
    pkg_path = os.path.dirname(secure_package_template.__file__)
    py_typed_path = os.path.join(pkg_path, "py.typed")
    assert os.path.isfile(py_typed_path)

def test_reload_preserves_version():
    # Re-import (reload) and ensure __version__ still exists
    import secure_package_template
    sys.modules.pop("secure_package_template")
    mod = importlib.import_module("secure_package_template")
    assert hasattr(mod, "__version__")
def test_version_module_importable():
    from secure_package_template import _version
    assert hasattr(_version, "__version__")
    assert _version.__version__ == "0.7.1"

def test_version_attribute_consistency():
    import secure_package_template
    from secure_package_template import _version
    assert secure_package_template.__version__ == _version.__version__

def test_import_version_str():
    import secure_package_template
    assert isinstance(secure_package_template.__version__, str)
    assert len(secure_package_template.__version__) > 0

def test_reload_package_preserves_version():
    import importlib
    import sys
    sys.modules.pop("secure_package_template")
    mod = importlib.import_module("secure_package_template")
    assert hasattr(mod, "__version__")
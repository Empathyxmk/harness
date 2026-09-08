def test_public_version_module_importable_and_format():
    from secure_package_template import _version
    assert hasattr(_version, "__version__")
    # In public test, check the version major is '0', minor is '7'
    v = _version.__version__
    parts = v.split(".")
    assert parts[0] == "0"
    assert parts[1] == "7"

def test_public_version_attribute_consistency_and_not_empty():
    import secure_package_template
    from secure_package_template import _version
    # Public: Check that attribute matches exactly and version isn't '0.0.0'
    assert secure_package_template.__version__ == _version.__version__
    assert secure_package_template.__version__ != "0.0.0"

def test_public_import_version_type_and_length():
    import secure_package_template
    ver = secure_package_template.__version__
    assert isinstance(ver, str)
    # Public: Check it's at least 5 chars long
    assert len(ver) >= 5

def test_public_reload_package_preserves_version_type():
    import importlib
    import sys
    sys.modules.pop("secure_package_template")
    mod = importlib.import_module("secure_package_template")
    # Instead of just hasattr, check it's alphanumeric with '.' present
    assert hasattr(mod, "__version__")
    version_str = getattr(mod, "__version__")
    assert "." in version_str
    assert version_str.replace(".", "").isalnum()
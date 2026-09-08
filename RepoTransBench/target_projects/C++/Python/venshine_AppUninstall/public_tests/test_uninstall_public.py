from src.appuninstall import uninstall

def test_remove_app_valid_package_removes_successfully():
    package_name = "com.example.anotherapp"
    result = uninstall.remove_app(package_name)
    assert result == 0

def test_remove_app_invalid_package_returns_error():
    package_name = "invalid.package.name.123"
    result = uninstall.remove_app(package_name)
    assert result == -1

def test_remove_app_empty_package_returns_error():
    package_name = ""
    result = uninstall.remove_app(package_name)
    assert result == -1
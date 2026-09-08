import pytest

def test_use_app_context():
    # Simulate Android context with a dict for testing
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.componentbase.test"
    assert app_context.package_name == "com.loong.componentbase.test"
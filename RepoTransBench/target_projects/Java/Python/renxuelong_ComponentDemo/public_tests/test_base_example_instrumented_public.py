def test_package_name_contains_base():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.base"
    assert "base" in app_context.package_name
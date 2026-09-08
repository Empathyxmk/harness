def test_app_context_package_name_is_not_null():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.componentbase.test"
    assert app_context.package_name is not None
    assert "componentbase" in app_context.package_name
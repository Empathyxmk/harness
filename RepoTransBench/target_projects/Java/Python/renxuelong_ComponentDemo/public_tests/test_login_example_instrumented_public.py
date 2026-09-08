def test_get_app_context_package_name_contains_login():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.login"
    assert "login" in app_context.package_name
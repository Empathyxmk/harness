def test_use_app_context_login():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.login"
    assert app_context.package_name == "com.loong.login"
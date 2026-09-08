def test_use_app_context_base():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.base.test"
    assert app_context.package_name == "com.loong.base.test"
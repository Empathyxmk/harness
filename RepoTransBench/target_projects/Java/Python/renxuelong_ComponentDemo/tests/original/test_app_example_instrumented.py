def test_use_app_context_componentdemo():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.componentdemo"
    assert app_context.package_name == "com.loong.componentdemo"
def test_use_app_context_share():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.share"
    assert app_context.package_name == "com.loong.share"
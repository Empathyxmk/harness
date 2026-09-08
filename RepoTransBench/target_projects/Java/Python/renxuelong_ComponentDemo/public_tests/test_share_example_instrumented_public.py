def test_app_context_package_name_contains_share():
    app_context = type('Ctx', (), {})()
    app_context.package_name = "com.loong.share"
    assert "share" in app_context.package_name
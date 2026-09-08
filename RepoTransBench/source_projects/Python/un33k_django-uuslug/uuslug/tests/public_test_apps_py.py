def test_apps_config_name_public():
    import uuslug.apps as apps_mod
    app_config = apps_mod.UuslugConfig("uuslug", "uuslug")
    # Should have correct name attribute
    assert app_config.name == "uuslug"
    # Check verbose_name is as expected but different assertion message/context
    assert hasattr(app_config, "verbose_name")
    assert app_config.verbose_name.lower().find("uuslug") >= 0
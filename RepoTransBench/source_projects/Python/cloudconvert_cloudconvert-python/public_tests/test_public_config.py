def test_config_imports_public():
    import cloudconvert.config as config_mod
    # Config must have at least these attributes
    assert hasattr(config_mod, "API_URL") or hasattr(config_mod, "SECRET_KEY")
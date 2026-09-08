import cloudconvert.config as config

def test_config_values():
    assert config.__version__ == "2.1.0"
    assert config.__pypi_packagename__ == "cloudconvert"
    assert "live" in config.__endpoint_map__
    assert "sandbox" in config.__sync_endpoint_map__
    assert config.SANDBOX_API_KEY.startswith("eyJ0")

def test_config_imports():
    # Test that import doesn't raise and variables exist
    assert hasattr(config, "__github_reponame__")
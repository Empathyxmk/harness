import pytest
from tiddl.config import Config

def test_config_defaults_public(tmp_path):
    # Use a dummy config dict with different test data
    data = {
        "auth": {
            "token": "public_token_abc",
            "user_id": "public_uid",
            "country_code": "DE"
        },
        "output_dir": str(tmp_path / "public_music"),
        "download": {
            "quality": "HI_RES_LOSSLESS",
            "concurrent_downloads": 8
        }
    }
    cfg = Config(**data)
    assert cfg.auth.token == "public_token_abc"
    assert cfg.auth.user_id == "public_uid"
    assert cfg.auth.country_code == "DE"
    assert "public_music" in cfg.output_dir
    assert cfg.download.quality == "HI_RES_LOSSLESS"
    assert cfg.download.concurrent_downloads == 8

def test_config_partial_data_public(tmp_path):
    # Provide only auth section, rest defaults
    data = {
        "auth": {
            "token": "another_token_xyz",
            "user_id": "another_uid",
            "country_code": "US"
        }
    }
    cfg = Config(**data)
    assert cfg.auth.token == "another_token_xyz"
    assert cfg.auth.user_id == "another_uid"
    assert cfg.auth.country_code == "US"
    # output_dir and download should fall back to defaults

def test_config_invalid_public():
    # Missing required auth fields, should raise
    with pytest.raises(Exception):
        Config(auth={"token": "missing_fields"})
import os
import tempfile
import json
from pathlib import Path
import tiddl.config as configmod


def test_templateconfig_defaults():
    tc = configmod.TemplateConfig()
    assert tc.track == "{artist} - {title}"
    assert tc.album.startswith("{album_artist}")
    assert isinstance(tc, configmod.TemplateConfig)


def test_downloadconfig_defaults():
    dc = configmod.DownloadConfig()
    assert dc.quality == "high"
    assert dc.path.name == "Tiddl"
    assert isinstance(dc, configmod.DownloadConfig)


def test_authconfig_defaults():
    ac = configmod.AuthConfig()
    assert ac.token == ""
    assert ac.refresh_token == ""
    assert isinstance(ac, configmod.AuthConfig)


def test_config_save_and_load(tmp_path, monkeypatch):
    # Patch ENV, CONFIG_PATH
    test_json = tmp_path / "tiddl.json"
    monkeypatch.setattr(configmod, "HOME_PATH", tmp_path)
    monkeypatch.setattr(configmod, "CONFIG_PATH", test_json)
    c = configmod.Config()
    c.auth.token = "tok"
    c.save()
    assert test_json.exists()
    with test_json.open() as f:
        j = json.load(f)
    assert j["auth"]["token"] == "tok"

    # re-load from file
    c2 = configmod.Config.fromFile()
    assert c2.auth.token == "tok"

def test_config_fromfile_returns_Config(tmp_path, monkeypatch):
    monkeypatch.setattr(configmod, "HOME_PATH", tmp_path)
    monkeypatch.setattr(configmod, "CONFIG_PATH", tmp_path / "tiddl.json")
    # Remove if exists
    if configmod.CONFIG_PATH.exists():
        configmod.CONFIG_PATH.unlink()
    # Should create a default config
    config = configmod.Config.fromFile()
    assert isinstance(config, configmod.Config)
    assert configmod.CONFIG_PATH.exists()

def test_config_fromfile_file_notfound(monkeypatch, tmp_path):
    monkeypatch.setattr(configmod, "HOME_PATH", tmp_path)
    monkeypatch.setattr(configmod, "CONFIG_PATH", tmp_path / "tiddl.json")
    # Ensure config doesn't exist
    if configmod.CONFIG_PATH.exists():
        configmod.CONFIG_PATH.unlink()
    config = configmod.Config.fromFile()
    assert isinstance(config, configmod.Config)
    assert configmod.CONFIG_PATH.exists()
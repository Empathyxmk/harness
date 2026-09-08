import os
import tempfile
import shutil
from pathlib import Path

import pytest

from protontricks import config

def test_config_get_set(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "myconf"
    cfg_dir.mkdir()
    config_file = cfg_dir / "protontricks" / "config.ini"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(cfg_dir))
    # Should not exist initially
    if config_file.exists():
        config_file.unlink()
    conf = config.Config()
    # Nonexistent returns default
    assert conf.get("section", "option", default=123) == 123

    conf.set("section", "option", "xyz")
    assert conf.get("section", "option") == "xyz"
    # File should be written
    assert config_file.exists()
    # Should persist after reload
    conf2 = config.Config()
    assert conf2.get("section", "option") == "xyz"

def test_config_file_not_found(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    # Ensure file does not exist
    config_file = tmp_path / "protontricks" / "config.ini"
    if config_file.exists():
        config_file.unlink()
    conf = config.Config()
    assert isinstance(conf, config.Config)  # Loads successfully
    assert conf.get("missing", "x", default=None) is None

def test_config_default_value(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    conf = config.Config()
    conf.set("sec", "opt", "val")
    assert conf.get("sec", "opt") == "val"
    assert conf.get("sec", "noopt", "def") == "def"

def test_get_config_returns_Config():
    c = config.get_config()
    assert isinstance(c, config.Config)
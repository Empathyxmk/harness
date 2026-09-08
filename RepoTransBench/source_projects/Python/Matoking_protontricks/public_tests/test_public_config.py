import os
import tempfile
from pathlib import Path

import pytest
from protontricks import config

def test_public_config_get_set(tmp_path, monkeypatch):
    # Use a custom XDG_CONFIG_HOME to avoid writing to real user config
    custom_config = tmp_path / "someconfig"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(custom_config))
    conf = config.Config()
    # Use different section/option than any existing test
    default_val = conf.get("publicsection", "optionnotset", default="some_public_default")
    assert default_val == "some_public_default"

    conf.set("publicsection", "publicopt", "vvvtest")
    assert conf.get("publicsection", "publicopt") == "vvvtest"

    # Changing value should persist
    conf.set("publicsection", "publicopt", "publicvalue2")
    assert conf.get("publicsection", "publicopt") == "publicvalue2"

    # Test that file is created and content is correct
    config_path = (
        Path(os.environ.get("XDG_CONFIG_HOME")) / "protontricks" / "config.ini"
    )
    assert config_path.exists()
    content = config_path.read_text()
    assert "publicsection" in content
    assert "publicopt" in content
    assert "publicvalue2" in content
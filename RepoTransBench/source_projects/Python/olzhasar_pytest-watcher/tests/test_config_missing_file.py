import pytest
from pytest_watcher.config import Config

def test_config_with_missing_file(tmp_path):
    config = Config(path=tmp_path / "notexisting.toml")
    # Check attribute that should always exist by dataclass definition
    assert hasattr(config, "path")

def test_config_fallback_default(tmp_path):
    config = Config(path=tmp_path / "notexisting2.toml")
    # There is no .get or ._data, but config uses dataclass fields as fallback
    assert config.path == tmp_path / "notexisting2.toml"
    assert config.runner == "pytest"
    assert config.delay == 0.2
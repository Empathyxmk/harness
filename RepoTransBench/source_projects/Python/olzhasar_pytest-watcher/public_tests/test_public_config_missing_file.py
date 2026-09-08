import pytest
from pytest_watcher.config import Config
from pathlib import Path

def test_config_file_not_existent():
    # Use a dummy nonexistent file path
    conf = Config(path=Path("surely_nonexistent_toml.toml"))
    assert conf.path.name == "surely_nonexistent_toml.toml"
    # Trying to load should raise
    with pytest.raises(Exception):
        conf.load()
from pytest_watcher.config import Config
import tempfile
from pathlib import Path

def test_config_custom_path():
    tmpfile = Path(tempfile.gettempdir()) / "different_test_pyproject.toml"
    tmpfile.write_text("[tool.pytest-watcher]\n")
    conf = Config(path=tmpfile)
    assert conf.path == tmpfile
    tmpfile.unlink()
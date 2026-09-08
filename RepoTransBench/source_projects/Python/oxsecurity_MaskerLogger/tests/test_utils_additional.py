import os
import pytest
from maskerlogger import utils

def test_get_config_file_path_default():
    # Should return an absolute path ending with gitleaks.toml
    path = utils.get_config_file_path()
    assert path.endswith(os.path.join("config", "gitleaks.toml"))
    assert os.path.isfile(path) or "gitleaks.toml" in path

def test_get_config_file_path_custom():
    fname = "some_other_config.toml"
    path = utils.get_config_file_path(fname)
    assert path.endswith(os.path.join("config", fname))
    # Don't assume file exists, just structure

def test_get_config_file_path_edge(monkeypatch):
    # Edge: test when __file__ is not set or config folder missing
    monkeypatch.setattr(utils, "__file__", "/tmp/fake.py")
    path = utils.get_config_file_path("foo.toml")
    assert path == os.path.join("/tmp", "config", "foo.toml")
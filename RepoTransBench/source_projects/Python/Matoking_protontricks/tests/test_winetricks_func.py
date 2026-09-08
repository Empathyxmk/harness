import os
from pathlib import Path
import shutil

import pytest

from protontricks import winetricks

def test_get_winetricks_path_env_var(monkeypatch, tmp_path, caplog):
    caplog.set_level("INFO")
    fake_path = tmp_path / "winetricks"
    fake_path.write_text("# fake winetricks\n")
    monkeypatch.setenv("WINETRICKS", str(fake_path))
    assert winetricks.get_winetricks_path() == fake_path

def test_get_winetricks_path_env_var_invalid(monkeypatch, tmp_path, caplog):
    caplog.set_level("ERROR")
    fake_path = tmp_path / "notexist"
    monkeypatch.setenv("WINETRICKS", str(fake_path))
    assert winetricks.get_winetricks_path() is None
    assert "invalid" in caplog.text

def test_get_winetricks_path_from_path(monkeypatch):
    monkeypatch.delenv("WINETRICKS", raising=False)
    called = []
    def fake_which(cmd):
        called.append(cmd)
        return "/usr/bin/winetricks"
    monkeypatch.setattr(shutil, "which", fake_which)
    val = winetricks.get_winetricks_path()
    assert isinstance(val, Path)
    assert str(val) == "/usr/bin/winetricks"
    assert called == ["winetricks"]

def test_get_winetricks_path_not_found(monkeypatch, caplog):
    monkeypatch.delenv("WINETRICKS", raising=False)
    caplog.set_level("ERROR")
    monkeypatch.setattr(shutil, "which", lambda cmd: None)
    assert winetricks.get_winetricks_path() is None
    assert "could not be found" in caplog.text
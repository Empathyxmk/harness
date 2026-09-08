import builtins
import types
from pathlib import Path
import tempfile
import shutil
import pytest

import cemu.settings

class PublicDummyConfigFile:
    def __init__(self, path):
        self.path = Path(path)
    def is_file(self):
        return True
    def write_text(self, txt):
        with self.path.open("w") as f:
            f.write(txt)
    def read_text(self):
        return self.path.read_text()
    def __fspath__(self):
        return str(self.path)

class PublicDummyTemplateConfig:
    def __init__(self, text):
        self.text = text
    def read_text(self):
        return self.text

def create_another_fake_configfile(tmpdir, initial_text="[Custom]\nexample = value\n"):
    userfile = Path(tmpdir) / "cemu.ini"
    with open(userfile, "w") as f:
        f.write(initial_text)
    return userfile

def test_settings_basic_public(tmp_path, monkeypatch):
    # Patch config paths/constants
    fake_ini = tmp_path / "cemu.ini"
    fake_template = tmp_path / "template-ini"
    fake_template.write_text("[PublicDefault]\nalpha = omega\n")
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_template)
    monkeypatch.setattr("cemu.const.DEBUG", True)

    if fake_ini.exists():
        fake_ini.unlink()

    s = cemu.settings.Settings()
    assert fake_ini.exists()
    assert s._Settings__config is not None

    s.set("SectionB", "key1", "val1")
    s.set("SectionB", "key2", "42")
    s.set("SectionB", "key3", "no")
    s.save()

    assert s.get("SectionB", "key1") == "val1"
    assert s.getint("SectionB", "key2") == 42
    assert s.getboolean("SectionB", "key3") is False

    assert "SectionB" in s
    assert "section-not-present" not in s

def test_settings_load_and_save_public(tmp_path, monkeypatch):
    fake_ini = create_another_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    monkeypatch.setattr("cemu.const.DEBUG", False)
    s = cemu.settings.Settings()
    s.set("Custom", "example", "public")
    s.save()
    s.load()
    assert s.get("Custom", "example") == "public"

def test_contains_public(tmp_path, monkeypatch):
    fake_ini = create_another_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    s = cemu.settings.Settings()
    assert "Custom" in s
    assert "nonexistent" not in s

def test_default_config_creation_public(tmp_path, monkeypatch):
    fake_ini = tmp_path / "cemu.ini"
    fake_template = tmp_path / "another-template"
    fake_template.write_text("[TemplateHere]\nhello=world\n")
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_template)
    monkeypatch.setattr("cemu.const.DEBUG", False)
    s = cemu.settings.Settings()
    assert "[TemplateHere]" in fake_ini.read_text()

def test_set_getint_getboolean_edge_public(tmp_path, monkeypatch):
    fake_ini = create_another_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    s = cemu.settings.Settings()
    s.set("EdgeTestInts", "notint", "xyz")
    s.set("EdgeTestBools", "notbool", "maybe")
    s.save()
    with pytest.raises(ValueError):
        s.getint("EdgeTestInts", "notint")
    with pytest.raises(ValueError):
        s.getboolean("EdgeTestBools", "notbool")
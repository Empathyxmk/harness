import builtins
import types
from pathlib import Path
import tempfile
import shutil

import cemu.settings

class DummyConfigFile:
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

class DummyTemplateConfig:
    def __init__(self, text):
        self.text = text
    def read_text(self):
        return self.text

def create_fake_configfile(tmpdir, initial_text="[General]\nfoo = bar\n"):
    userfile = Path(tmpdir) / "cemu.ini"
    with open(userfile, "w") as f:
        f.write(initial_text)
    return userfile

def test_settings_basic(tmp_path, monkeypatch):
    # Patch out config paths/constants
    fake_ini = tmp_path / "cemu.ini"
    fake_template = tmp_path / "template-ini"
    fake_template.write_text("[_DEFAULT_]\ndefault = val\n")
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_template)
    monkeypatch.setattr("cemu.const.DEBUG", True) # So that dbg will run

    # Remove if exists to test file creation
    if fake_ini.exists():
        fake_ini.unlink()

    s = cemu.settings.Settings()
    # The file should now exist
    assert fake_ini.exists()
    # Should load from file
    assert s._Settings__config is not None

    s.set("SectionA", "foo", "bar")
    s.set("SectionA", "bar", "17")
    s.set("SectionA", "baz", "yes")
    s.save()

    # Now we can get values
    assert s.get("SectionA", "foo") == "bar"
    assert s.getint("SectionA", "bar") == 17
    assert s.getboolean("SectionA", "baz") is True

    # Test contains
    assert "SectionA" in s
    assert "not-exist" not in s

def test_settings_load_and_save(tmp_path, monkeypatch):
    fake_ini = create_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    monkeypatch.setattr("cemu.const.DEBUG", False)
    s = cemu.settings.Settings()
    s.set("General", "foo", "baz")
    s.save()
    s.load()
    assert s.get("General", "foo") == "baz"

def test_contains(tmp_path, monkeypatch):
    fake_ini = create_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    s = cemu.settings.Settings()
    assert "General" in s
    assert "missing" not in s

def test_default_config_creation(tmp_path, monkeypatch):
    # Simulate missing config file
    fake_ini = tmp_path / "cemu.ini"
    fake_template = tmp_path / "template-ini"
    fake_template.write_text("[JustATemplate]\nbar=foo\n")
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_template)
    monkeypatch.setattr("cemu.const.DEBUG", False)
    s = cemu.settings.Settings()
    # Config file should now exist and contain the template content
    assert "[JustATemplate]" in fake_ini.read_text()

def test_set_getint_getboolean_edge(tmp_path, monkeypatch):
    fake_ini = create_fake_configfile(tmp_path)
    monkeypatch.setattr("cemu.const.CONFIG_FILEPATH", fake_ini)
    monkeypatch.setattr("cemu.const.TEMPLATE_CONFIG", fake_ini)
    s = cemu.settings.Settings()
    s.set("Ints", "ival", "xnotanint")
    s.set("Bools", "bval", "xnotabool")
    s.save()
    with pytest.raises(ValueError):
        s.getint("Ints", "ival")
    with pytest.raises(ValueError):
        s.getboolean("Bools", "bval")
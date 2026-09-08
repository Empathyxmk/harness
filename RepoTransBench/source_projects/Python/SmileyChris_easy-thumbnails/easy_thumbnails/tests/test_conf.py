import pytest
from easy_thumbnails import conf

def test_appsettings_revert_resets(monkeypatch):
    django_settings = type(
        "Settings", (), {"FOO": "bar", "BAR": "baz"})
    monkeypatch.setattr(conf, "django_settings", django_settings)
    appsettings = conf.AppSettings()
    appsettings.FOO = "new"
    appsettings.BAR = "else"
    appsettings.revert()
    assert django_settings.FOO == "bar"
    assert django_settings.BAR == "baz"

def test_appsettings_isolated(monkeypatch):
    appsettings = conf.AppSettings(isolated=True)
    appsettings.FOO = 321
    assert appsettings.FOO == 321
    appsettings.revert()
    # Should still clear isolated overrides
    appsettings.FOO = 123
    assert appsettings.FOO == 123

def test_appsettings_fallback(monkeypatch):
    # If not isolated and attribute missing, should fall back to defaults or error
    django_settings = type(
        "DjangoSettings", (), {})()
    monkeypatch.setattr(conf, "django_settings", django_settings)
    appsettings = conf.AppSettings(isolated=False)
    appsettings.MYSET = 42
    assert conf.django_settings.MYSET == 42

def test_settings_default_values():
    s = conf.Settings()
    assert not s.THUMBNAIL_DEBUG
    assert s.THUMBNAIL_DEFAULT_STORAGE
    assert hasattr(s, "THUMBNAIL_BASEDIR")

def test_appsettings_set_get(monkeypatch):
    appsettings = conf.AppSettings(isolated=True)
    appsettings.MYFOO = 1
    assert appsettings.MYFOO == 1
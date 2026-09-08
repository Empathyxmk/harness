import pytest
from freezegun import config

def test_settings_default():
    s = config.Settings()
    assert isinstance(s.default_ignore_list, list)
    assert 'nose.plugins' in s.default_ignore_list

def test_settings_custom_ignore_list():
    custom = ['foo', 'bar']
    s = config.Settings(custom)
    assert s.default_ignore_list == custom

def test_configure_default_ignore_replacement():
    orig = config.settings.default_ignore_list[:]
    new_list = ['abc', 'def']
    config.configure(default_ignore_list=new_list)
    assert config.settings.default_ignore_list == new_list
    config.reset_config()
    assert config.settings.default_ignore_list == config.DEFAULT_IGNORE_LIST

def test_configure_extend_ignore_list():
    config.reset_config()
    base = config.settings.default_ignore_list[:]
    to_add = ['foo', 'bar']
    config.configure(extend_ignore_list=to_add)
    assert 'foo' in config.settings.default_ignore_list
    assert 'bar' in config.settings.default_ignore_list
    for item in base:
        assert item in config.settings.default_ignore_list
    # no duplicates
    config.configure(extend_ignore_list=['foo'])
    assert config.settings.default_ignore_list.count('foo') == 1

def test_configure_mutual_exclusion():
    with pytest.raises(config.ConfigurationError):
        config.configure(default_ignore_list=['a'], extend_ignore_list=['b'])

def test_reset_config_restores_defaults():
    config.configure(default_ignore_list=['abc'])
    config.reset_config()
    assert config.settings.default_ignore_list == config.DEFAULT_IGNORE_LIST
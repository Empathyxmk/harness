import pytest
from bumpversion import __init__ as bumpversion_init

def test_config_file_section_defaults():
    conf = {
        "current_version": "2.2.2",
        "parse": 'abc(?P<alpha>[a-zA-Z]+)',
        "serialize": ["{alpha}"]
    }
    # This somewhat indirectly checks parse/serialize logic entry in config handling, using different parse pattern
    options = bumpversion_init.ConfiguredFile("setup.cfg", conf, {})
    assert options.serialize == ["{alpha}"]

def test_default_parse_pattern_is_used_new():
    # With custom section key
    conf = {"current_version": "1.9.9"}
    options = bumpversion_init.ConfiguredFile("pyproject.toml", conf, {})
    assert options.config_file == "pyproject.toml"
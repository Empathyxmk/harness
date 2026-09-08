from src.PropTypes import PropTypes, style_validator, config_style_validator

def test_validates_allowed_style_properties_public():
    props = {'style': {'color': 'purple'}}
    try:
        result = PropTypes.style(props['style'])
        assert result is None
    except Exception:
        assert False, "Should not error for allowed style"

def test_triggers_warning_on_wrong_type_pattern_public():
    props = {'style': 1234}
    try:
        PropTypes.style(props['style'])
        assert False, "Expected exception for non-dict style"
    except Exception as e:
        msg = str(e)
        assert "Invalid style" in msg
        assert "dict" in msg

def test_calls_style_validator_for_style_object_public(monkeypatch):
    called = []
    orig_validate = style_validator.validate
    def fake_validate(style, comp):
        called.append((style, comp))
        return None
    style_validator.validate = fake_validate
    props = {'style': {'background': '#fff'}}
    PropTypes.style(props['style'])
    assert called and called[-1][0] == {'background': '#fff'}
    style_validator.validate = orig_validate

def test_config_style_validator_modifies_config_public(monkeypatch):
    called = []
    orig_set_config = style_validator.setConfig
    def fake_set_config(cfg):
        called.append(cfg)
    style_validator.setConfig = fake_set_config
    config = {'customWarn': True}
    config_style_validator(config)
    assert called and called[-1] == config
    style_validator.setConfig = orig_set_config
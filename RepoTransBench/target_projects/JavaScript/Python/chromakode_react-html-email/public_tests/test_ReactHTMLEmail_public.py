from src import index as module

def test_proptype_style_error_for_non_objects_public():
    style = "not-an-object"
    try:
        module.PropTypes.style(style)
        assert False, "Expected exception for invalid style type"
    except Exception as e:
        msg = str(e)
        assert "Invalid style" in msg

def test_validates_different_style_objects_public(monkeypatch):
    calls = []
    orig_validate = module.default.styleValidator.validate
    def fake_validate(style, component):
        calls.append((style, component))
        return None
    module.default.styleValidator.validate = fake_validate
    style = {"padding": "5px"}
    module.PropTypes.style(style)
    assert calls and calls[-1][0] == style
    module.default.styleValidator.validate = orig_validate

def test_config_style_validator_updates_config_different_config_public(monkeypatch):
    calls = []
    orig_set_config = module.default.styleValidator.setConfig
    def fake_set_config(cfg):
        calls.append(cfg)
    module.default.styleValidator.setConfig = fake_set_config
    config = {'strict': True}
    module.configStyleValidator(config)
    assert calls and calls[-1] == config
    module.default.styleValidator.setConfig = orig_set_config

def test_when_node_env_production_public(monkeypatch):
    import os
    orig = os.environ.get('NODE_ENV')
    os.environ['NODE_ENV'] = 'production'
    module.default.styleValidator.config['warn'] = False
    assert module.default.styleValidator.config['warn'] == False
    if orig is not None:
        os.environ['NODE_ENV'] = orig
    else:
        del os.environ['NODE_ENV']
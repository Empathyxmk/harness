import pytest
from src.zapv2 import ruleConfig as ruleConfig_module

class DummyZAP:
    def __init__(self):
        self.base = 'BASE/'
        self.called = []
    def _request(self, url, params=None):
        self.called.append((url, params))
        return {'value': 'dummy'}

@pytest.fixture
def ruleconfig():
    return ruleConfig_module.ruleConfig(DummyZAP())

def test_rule_config_value(ruleconfig):
    r = ruleconfig.rule_config_value('key1')
    assert r == 'dummy'

def test_all_rule_configs(ruleconfig):
    v = ruleconfig.all_rule_configs
    assert v == 'dummy'

def test_reset_rule_config_value(ruleconfig):
    v = ruleconfig.reset_rule_config_value('key2')
    assert v == 'dummy'

def test_reset_all_rule_config_values(ruleconfig):
    v = ruleconfig.reset_all_rule_config_values()
    assert v == 'dummy'

def test_set_rule_config_value_without_value(ruleconfig):
    v = ruleconfig.set_rule_config_value('key3')
    assert v == 'dummy'

def test_set_rule_config_value_with_value(ruleconfig):
    v = ruleconfig.set_rule_config_value('key4', value='somevalue')
    assert v == 'dummy'
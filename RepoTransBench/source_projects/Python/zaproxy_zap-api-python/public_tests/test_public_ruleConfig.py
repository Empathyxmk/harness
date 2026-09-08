import sys
import os
import pytest

# Ensure src directory is on PYTHONPATH for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from zapv2 import ruleConfig as ruleConfig_module

def test_rule_config_set_and_get_diff_data():
    rule_id = "12001"
    key = "attackStrength"
    value = "LOW"
    set_resp = ruleConfig_module.set_rule_config_value(rule_id, key, value)
    assert set_resp["status"] == "UPDATED"
    assert set_resp["ruleId"] == rule_id

    get_resp = ruleConfig_module.get_rule_config_value(rule_id, key)
    assert get_resp["value"] == value
    assert get_resp["key"] == key
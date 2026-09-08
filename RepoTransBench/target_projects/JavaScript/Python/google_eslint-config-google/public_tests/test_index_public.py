# Purpose: Public tests for index.py exports and rule structure (different test data)

import importlib
import types

import pytest

import sys
import os

# Dynamically import the index.py module from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
conf = importlib.import_module('index')

def test_should_export_a_non_null_object():
    assert conf is not None and isinstance(conf, types.ModuleType) or isinstance(conf, object)
    assert hasattr(conf, 'rules')
    assert isinstance(conf.rules, dict)

def test_should_include_a_different_set_of_specific_rules():
    # 'quotes' is present and is an array, contains 'error'
    assert 'quotes' in conf.rules
    assert isinstance(conf.rules['quotes'], list)
    assert conf.rules['quotes'][0] == 'error'

    # 'indent' is present and is an array
    assert 'indent' in conf.rules
    assert isinstance(conf.rules['indent'], list)
    assert conf.rules['indent'][0] == 'error'
    assert isinstance(conf.rules['indent'][1], int)

    # 'array-bracket-newline' is set to 'off'
    assert 'array-bracket-newline' in conf.rules and conf.rules['array-bracket-newline'] == 'off'

def test_should_still_omit_other_commented_out_rules():
    assert 'no-alert' not in conf.rules
    assert 'no-script-url' not in conf.rules

def test_should_have_a_decent_number_of_rule_keys_threshold_public():
    assert len(list(conf.rules.keys())) > 10
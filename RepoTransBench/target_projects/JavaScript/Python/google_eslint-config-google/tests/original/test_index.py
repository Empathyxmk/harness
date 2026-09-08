# Purpose: Directly test index.py exports and rule structure
import importlib
import types

import pytest

import sys
import os

# Dynamically import the index.py module from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
conf = importlib.import_module('index')

def test_should_export_an_object():
    assert isinstance(conf, types.ModuleType) or isinstance(conf, object)
    assert hasattr(conf, 'rules')
    assert isinstance(conf.rules, dict)

def test_should_include_specific_rules():
    # Test for some explicit rules
    assert 'no-cond-assign' in conf.rules and conf.rules['no-cond-assign'] == 'off'
    assert 'no-irregular-whitespace' in conf.rules and conf.rules['no-irregular-whitespace'] == 'error'
    assert 'no-unexpected-multiline' in conf.rules and conf.rules['no-unexpected-multiline'] == 'error'
    assert 'curly' in conf.rules
    assert isinstance(conf.rules['curly'], list)
    assert conf.rules['curly'][0] == 'error'
    assert conf.rules['curly'][1] == 'multi-line'

def test_should_not_override_commented_out_rules():
    # A commented out rule should not be present (as a string rule only).
    assert 'no-console' not in conf.rules
    assert 'no-empty-character_class' not in conf.rules and 'no-empty-character-class' not in conf.rules  # handle both (js typo)

def test_should_not_crash_when_listing_all_rule_keys():
    assert len(list(conf.rules.keys())) > 0
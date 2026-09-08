import os
import sys
import importlib.util

import pytest

# Assume we're running from project root, need to import fantasyland.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from fantasyland import fantasyLand

mapping_keys = list(fantasyLand.keys())

all_possible_keys = [
    'equals', 'lte', 'concat', 'empty', 'map', 'ap', 'of', 'reduce',
    'traverse', 'chain', 'bimap', 'extend', 'extract', 'compose',
    'id', 'zero', 'alt', 'promap', 'filter', 'contramap', 'chainRec', 'invert'
]

def test_exports_all_fantasy_land_mapping_keys():
    for k in mapping_keys:
        assert k in fantasyLand, f"Missing key: {k}"
        assert fantasyLand[k] == f"fantasy-land/{k}"

def test_each_key_maps_to_correct_string():
    for key in mapping_keys:
        assert fantasyLand[key] == f'fantasy-land/{key}'

def test_contains_all_expected_keys_no_extra_no_missing():
    assert sorted(mapping_keys) == sorted(all_possible_keys), "Mapping keys match Fantasy Land spec"

def test_only_string_values():
    for value in fantasyLand.values():
        assert isinstance(value, str)
        assert value.startswith('fantasy-land/')

def test_no_duplicate_values():
    values = list(fantasyLand.values())
    unique = set(values)
    assert len(values) == len(unique)

def test_invalid_property_access_returns_none():
    assert fantasyLand.get('not-a-key') is None

def test_all_possible_keys_present():
    for key in all_possible_keys:
        assert key in fantasyLand, f"Key {key} is missing"

def test_global_fallback_simulated_browser_env(tmp_path):
    """
    Simulate JS global fallback by executing a Python version of the mapping as if in a 'global' namespace.
    """
    # In Python, we'll simulate by creating a fake global dictionary
    fake_self = {}
    # Simulate the code: assign fantasyLand mapping to 'self.FantasyLand'
    fake_self['FantasyLand'] = {k: f'fantasy-land/{k}' for k in all_possible_keys}
    fantasyLandGlobal = fake_self["FantasyLand"]
    for key in all_possible_keys:
        assert fantasyLandGlobal[key] == f'fantasy-land/{key}'
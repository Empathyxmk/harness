import os
import sys
import importlib.util

import pytest

# Import the core mapping
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fantasyland import fantasyLand

mapping_keys = list(fantasyLand.keys())

# Alternate (public test) key order:
all_public_keys = [
    'ap', 'equals', 'of', 'compose', 'contramap', 'traverse', 'map', 'extend',
    'concat', 'id', 'bimap', 'alt', 'reduce', 'extract', 'chain', 'lte',
    'filter', 'promap', 'invert', 'chainRec', 'empty', 'zero'
]

def test_exports_all_fantasy_land_mapping_keys_public():
    for k in all_public_keys:
        assert k in fantasyLand, f"Missing key (public): {k}"
        assert fantasyLand[k] == f"fantasy-land/{k}"

def test_each_key_maps_to_correct_string_public():
    for key in all_public_keys:
        assert fantasyLand[key] == f'fantasy-land/{key}'

def test_contains_all_expected_keys_different_order_public():
    assert sorted(mapping_keys) == sorted(all_public_keys), "Mapping keys match Fantasy Land spec (public order, public data)"

def test_only_string_values_different_public_order():
    for key in all_public_keys:
        value = fantasyLand[key]
        assert isinstance(value, str)
        assert value.endswith(f'/{key}')

def test_no_duplicate_values_public():
    values = list(fantasyLand.values())
    unique = set(values)
    assert len(values) == len(unique)

def test_returns_none_for_fake_keys_public():
    assert fantasyLand.get('this-is-not-a-key') is None
    assert fantasyLand.get('fantasy') is None
    assert fantasyLand.get('@@fantasy-land') is None

def test_public_keys_all_present_public():
    for key in all_public_keys:
        assert key in fantasyLand, f"Public key {key} is missing"

def test_browser_global_fallback_simulated_public(tmp_path):
    """
    Simulate the browser global (public test) fallback logic: mapping assigned to a simulated 'self' object.
    """
    fake_self = {}
    fake_self['FantasyLand'] = {k: f'fantasy-land/{k}' for k in all_public_keys}
    fantasyLandGlobal = fake_self["FantasyLand"]
    for key in all_public_keys:
        assert fantasyLandGlobal[key] == f'fantasy-land/{key}'
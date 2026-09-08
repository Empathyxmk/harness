import sys
import os
import pytest

# Add the parent directory to sys.path to import jsons
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jsons

def test_loads_dict_with_integers():
    data = '{"g": 20, "h": 30}'
    loaded = jsons.loads(data)
    assert loaded == {"g": 20, "h": 30}

def test_loads_dict_with_string_and_float():
    data = '{"x": "value", "y": 33.8}'
    loaded = jsons.loads(data)
    assert loaded == {"x": "value", "y": 33.8}

def test_dumps_dict_with_varied_types():
    data = {"planet": "Earth", "moons": 1, "has_life": True}
    dumped = jsons.dumps(data)
    assert '"planet": "Earth"' in dumped
    assert '"moons": 1' in dumped
    assert '"has_life": true' in dumped
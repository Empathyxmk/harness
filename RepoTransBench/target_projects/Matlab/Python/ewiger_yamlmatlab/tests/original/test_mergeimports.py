import pytest
from yamlmatlab import yaml

def test_merge_value_and_other():
    x = {'val': 1}
    y = {'val': 2, 'other': 42}
    z = yaml.mergeimports(x, y)
    assert z['val'] == 2 and z['other'] == 42

def test_merge_empty_structs():
    z2 = yaml.mergeimports({}, {})
    assert isinstance(z2, dict)
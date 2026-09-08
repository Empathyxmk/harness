import pytest
from yamlmatlab import yaml

def test_merge_struct_basic():
    s1 = {'a': 1, 'b': 2}
    s2 = {'b': 8, 'c': 9}
    out = yaml.merge_struct(s1, s2)
    assert out['a'] == 1 and out['b'] == 8 and out['c'] == 9
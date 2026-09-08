import pytest
from yamlmatlab import yaml

def test_basic_yaml_parse():
    r = yaml.ReadYamlRaw('num: 5')
    assert isinstance(r, dict) and 'num' in r and r['num'] == 5

def test_empty_yaml_input():
    empty = yaml.ReadYamlRaw('')
    assert empty == {} or len(getattr(empty, 'keys', lambda:[])()) == 0

def test_malformed_yaml_raises():
    with pytest.raises(Exception):
        yaml.ReadYamlRaw('a: [b: c]')

def test_nested_yaml_parse():
    s = yaml.ReadYamlRaw('foo:\n  bar: true\n  baz: [1,2,3]')
    assert 'foo' in s and 'bar' in s['foo']
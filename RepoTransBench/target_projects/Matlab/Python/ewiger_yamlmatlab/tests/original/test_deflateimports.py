import pytest
from yamlmatlab import yaml

def test_list_imports():
    s = {'import': [{'x': 1}, {'y': 2}], 'item': 5}
    out = yaml.deflateimports(s)
    assert isinstance(out, dict)
    assert 'import' in out and 'item' in out

def test_empty_struct():
    e = {}
    out2 = yaml.deflateimports(e)
    assert isinstance(out2, dict)

def test_non_import_struct():
    s2 = {'foo': 1}
    o3 = yaml.deflateimports(s2)
    assert 'foo' in o3
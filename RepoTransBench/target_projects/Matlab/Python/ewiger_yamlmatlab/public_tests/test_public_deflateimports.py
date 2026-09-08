from yamlmatlab import yaml

def test_public_list_imports():
    s = {'import': [{'a': 10}, {'b': 20}], 'item': 50}
    out = yaml.deflateimports(s)
    assert isinstance(out, dict)
    assert 'import' in out and 'item' in out

def test_public_empty_struct():
    e = {}
    out2 = yaml.deflateimports(e)
    assert isinstance(out2, dict)

def test_public_non_import_struct():
    s2 = {'bar': 99}
    o3 = yaml.deflateimports(s2)
    assert 'bar' in o3
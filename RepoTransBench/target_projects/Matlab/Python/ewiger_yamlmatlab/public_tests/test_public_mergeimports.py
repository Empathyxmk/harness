from yamlmatlab import yaml

def test_public_basic_mergeimports():
    a = {'d': 99, 'e': 88}
    b = {'e': 777, 'f': 111}
    c = yaml.mergeimports(a, b)
    assert 'd' in c and 'e' in c and 'f' in c
    assert c['e'] == 777 and c['f'] == 111 and c['d'] == 99

def test_public_overwrite_mergeimports():
    a = {'foo': 50}
    b = {'foo': 51, 'bar': 52}
    c = yaml.mergeimports(a, b)
    assert c['foo'] == 51 and c['bar'] == 52

def test_public_mergeimports_with_empty():
    a = {}
    b = {'x': 42}
    c = yaml.mergeimports(a, b)
    assert c['x'] == 42
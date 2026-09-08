from yamlmatlab import yaml

def test_public_non_overlapping_fields():
    s1 = {'foo': 123, 'baz': 555}
    s2 = {'other': 789, 'extra': 444}
    s = yaml.merge_struct(s1, s2)
    assert 'foo' in s and 'other' in s
    assert s['foo'] == 123 and s['other'] == 789 and s['extra'] == 444

def test_public_field_overwrite():
    s1 = {'x': 1, 'z': 15}
    s2 = {'x': 99, 'y': 2}
    s = yaml.merge_struct(s1, s2)
    assert s['x'] == 99 and s['y'] == 2 and s['z'] == 15

def test_public_empty_struct():
    s1 = {}
    s2 = {'k': 7}
    s = yaml.merge_struct(s1, s2)
    assert s['k'] == 7
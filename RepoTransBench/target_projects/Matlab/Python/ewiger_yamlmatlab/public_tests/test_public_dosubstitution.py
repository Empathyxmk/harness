from yamlmatlab import yaml

def test_public_substitution():
    # Substitute $baz in string with actual value, different variable name
    s = {'baz': 'qux', 'text': 'Value is $baz'}
    result = yaml.dosubstitution(s, s)
    assert 'text' in result
    assert 'qux' in result['text']

def test_public_simple_field_substitution():
    s2 = {'animal': 'dog'}
    result = yaml.dosubstitution({'pet': '$animal'}, s2)
    assert result['pet'] == 'dog'

def test_public_missing_var_substitution():
    s3 = {'field': '$nonexistent'}
    r = yaml.dosubstitution(s3, {'nothere': 2})
    assert isinstance(r['field'], str)
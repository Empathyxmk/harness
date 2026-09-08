import pytest
from yamlmatlab import yaml

def test_basic_substitution():
    # Substitute $foo in string with actual value
    s = {'foo': 'bar', 'text': 'Value is $foo'}
    result = yaml.dosubstitution(s, s)
    assert 'text' in result
    assert 'bar' in result['text']

def test_simple_field_substitution():
    s2 = {'foo': 'bar'}
    result = yaml.dosubstitution({'field': '$foo'}, s2)
    assert result['field'] == 'bar'

def test_missing_var_substitution():
    s3 = {'field': '$missing'}
    r = yaml.dosubstitution(s3, {'notthere': 1})
    assert isinstance(r['field'], str)
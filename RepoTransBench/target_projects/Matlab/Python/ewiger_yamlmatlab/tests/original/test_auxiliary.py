import pytest
from yamlmatlab import yaml

def test_iscolumnvector_isrowvector():
    a = [1, 2, 3, 4, 5]
    b = [1, 2, 3, 4, 5]
    assert yaml.iscolumnvector([[x] for x in a])
    assert not yaml.iscolumnvector(b)
    assert yaml.isrowvector(b)
    assert not yaml.isrowvector([[x] for x in a])

def test_ismymatrix():
    m = [[1, 2], [3, 4]]
    a = [[1], [2], [3], [4], [5]]
    assert yaml.ismymatrix(m)
    assert not yaml.ismymatrix(a)

def test_isord():
    assert yaml.isord([1, 2, 3])
    assert not yaml.isord([1, 3, 2])

def test_issingle():
    assert yaml.issingle(5)
    assert not yaml.issingle([2, 3])

def test_kwd_parent():
    parent = yaml.kwd_parent('import', {'import': True})
    assert parent == 'import'

def test_datadump():
    out = yaml.datadump([1, 2, 3])
    assert isinstance(out, str)
    out2 = yaml.datadump({'x': 1})
    assert isinstance(out2, str)

def test_extras_GetYamlVals():
    testS = {'a': 1, 'b': {'c': 2}}
    vals = yaml.extras.GetYamlVals(testS)
    assert isinstance(vals, dict)

def test_extras_TimeVals2Cell():
    tc = yaml.extras.TimeVals2Cell(['2021-01-01T00:00:00', '2022-02-02T12:00:10'])
    assert isinstance(tc, list)
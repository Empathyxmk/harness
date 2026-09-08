import pytest
from yamlmatlab import yaml

def test_default_constructor():
    d0 = yaml.DateTime()
    strd0 = str(d0)
    assert isinstance(strd0, (str,))

def test_date_string_constructor():
    d1 = yaml.DateTime('2020-12-31 23:59:59')
    assert str(d1) == '2020-12-31T23:59:59'

def test_ymdhms_constructor():
    d2 = yaml.DateTime(2023, 6, 19, 14, 33, 59)
    assert '2023-06-19T14:33:59' in str(d2)

def test_datenum_constructor():
    import datetime
    now = datetime.datetime.now()
    d3 = yaml.DateTime(now)
    assert isinstance(str(d3), str)

def test_relational_operators():
    dA = yaml.DateTime('2021-01-01T12:00:00')
    dB = yaml.DateTime('2021-01-01T13:00:00')
    assert (dA < dB) and not (dB < dA)
    assert (dA <= dB) and (dA <= dA) and not (dB <= dA)
    assert (dA != dB) and (dA == dA)

def test_bad_input_raises():
    with pytest.raises(Exception):
        yaml.DateTime('invalid-date-string')
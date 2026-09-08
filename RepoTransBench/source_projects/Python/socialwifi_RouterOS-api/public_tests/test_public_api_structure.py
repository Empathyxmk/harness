import datetime
import ipaddress
import pytest

from routeros_api import api_structure

def test_string_field_different_string():
    field = api_structure.StringField()
    test_str = "hello world!"
    as_bytes = field.get_mikrotik_value(test_str)
    assert as_bytes == b"hello world!"
    assert field.get_python_value(as_bytes) == test_str

def test_bytes_field_random_bytes():
    field = api_structure.BytesField()
    val = b"random_bytes123"
    assert field.get_mikrotik_value(val) == val
    assert field.get_python_value(val) == val

def test_boolean_field_variants():
    field = api_structure.BooleanField()
    assert field.get_mikrotik_value(True) == b'yes'
    assert field.get_mikrotik_value(False) == b'no'
    assert field.get_python_value(b'true') is True
    assert field.get_python_value(b'no') is False

def test_integer_field_various():
    field = api_structure.IntegerField()
    assert field.get_mikrotik_value(12345) == b'12345'
    assert field.get_python_value(b'6789') == 6789

def test_timedelta_field_and_parse_other_format():
    field = api_structure.TimedeltaField()
    td = datetime.timedelta(days=1, hours=2, minutes=3, seconds=4)
    mk = field.get_mikrotik_value(td)
    assert mk == b'93784s'
    assert field.get_python_value(b'2h3m') == datetime.timedelta(hours=2, minutes=3)
    assert field.get_python_value(b'none') is None

def test_timedelta_parse_old_format():
    field = api_structure.TimedeltaField()
    assert field.get_python_value(b'1w2d03:14:07') == datetime.timedelta(
        weeks=1, days=2, hours=3, minutes=14, seconds=7
    )

def test_ipnetwork_field_and_empty():
    field = api_structure.IpNetworkField()
    n = ipaddress.ip_network('10.0.0.0/8')
    as_bytes = field.get_mikrotik_value(n)
    assert as_bytes == b'10.0.0.0/8'
    n2 = field.get_python_value(b'192.168.100.0/24')
    assert str(n2) == '192.168.100.0/24'
    assert field.get_mikrotik_value(None) == b''
    assert field.get_python_value(b'') is None

def test_list_field_with_string():
    subfield = api_structure.StringField()
    field = api_structure.ListField(subfield)
    l = ['one', 'two', 'three']
    expected = b'one,two,three'
    assert field.get_mikrotik_value(l) == expected
    l2 = field.get_python_value(b'apple,banana')
    assert l2 == ['apple', 'banana']

def test_list_field_with_single_element():
    subfield = api_structure.StringField()
    field = api_structure.ListField(subfield)
    assert field.get_python_value(b'cherry') == ['cherry']

def test_timedelta_invalid_value():
    field = api_structure.TimedeltaField()
    with pytest.raises(ValueError):
        field.get_python_value(b'invalidformat')
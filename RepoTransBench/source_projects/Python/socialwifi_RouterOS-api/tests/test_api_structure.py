import pytest
import datetime
import ipaddress
from routeros_api import api_structure

def test_string_field_encoding():
    f = api_structure.StringField(encoding='utf-8')
    s = 'ąćę'
    val = f.get_mikrotik_value(s)
    assert isinstance(val, bytes)
    s2 = f.get_python_value(val)
    assert s2 == s

def test_bytes_field_roundtrip():
    f = api_structure.BytesField()
    data = b'abc'
    assert f.get_mikrotik_value(data) == data
    assert f.get_python_value(data) == data

def test_boolean_field_true_false():
    f = api_structure.BooleanField()
    assert f.get_mikrotik_value(True) == b'yes'
    assert f.get_mikrotik_value(False) == b'no'
    assert f.get_python_value(b'yes') is True
    assert f.get_python_value(b'true') is True
    assert f.get_python_value(b'no') is False
    assert f.get_python_value(b'false') is False
    with pytest.raises(AssertionError):
        f.get_python_value(b'notvalid')

def test_integer_field():
    f = api_structure.IntegerField()
    val = f.get_mikrotik_value(42)
    assert val == b'42'
    assert f.get_python_value(b'42') == 42

def test_timedelta_field_none_and_seconds():
    f = api_structure.TimedeltaField()
    assert f.get_mikrotik_value(None) == b'none'
    td = datetime.timedelta(seconds=10)
    assert f.get_mikrotik_value(td) == b'10s'
    assert f.get_python_value(b'none') is None
    # new format
    assert f.get_python_value(b'2d3h4m5s6ms') == datetime.timedelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6)
    # old format
    assert f.get_python_value(b'1w2d03:04:05.006') == datetime.timedelta(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=6)
    # invalid format
    with pytest.raises(ValueError):
        f.get_python_value(b'invalid')

def test_ipnetwork_field():
    f = api_structure.IpNetworkField()
    assert f.get_mikrotik_value(ipaddress.ip_network('10.0.0.0/24')) == b'10.0.0.0/24'
    assert f.get_mikrotik_value(None) == b''
    assert f.get_python_value(b'10.0.0.0/24') == ipaddress.ip_network('10.0.0.0/24')
    assert f.get_python_value(b'') is None

def test_list_field():
    subfield = api_structure.StringField()
    f = api_structure.ListField(subfield)
    val = f.get_mikrotik_value(['a','b','c'])
    assert val == b'a,b,c'
    assert f.get_python_value(b'a,b,c') == ['a','b','c']
    fsemi = api_structure.ListField(subfield)
    assert fsemi.get_python_value(b'a;b;c') == ['a','b','c']

def test_default_structure():
    struct = api_structure.default_structure
    assert isinstance(struct['anykey'], api_structure.StringField)

class DummyField(api_structure.Field):
    def get_mikrotik_value(self, arg):
        return b''

    def get_python_value(self, arg):
        return arg

def test_abstract_methods_raise():
    class F(api_structure.Field):
        def get_mikrotik_value(self, arg): return super().get_mikrotik_value(arg)
        def get_python_value(self, arg): return super().get_python_value(arg)
    with pytest.raises(NotImplementedError):
        F().get_mikrotik_value(None)
    with pytest.raises(NotImplementedError):
        F().get_python_value(None)
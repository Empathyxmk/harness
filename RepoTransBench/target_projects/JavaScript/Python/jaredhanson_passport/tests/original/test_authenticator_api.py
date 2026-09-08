import pytest

class Authenticator:
    def __init__(self):
        self._strategies = {}
        self._key = 'passport'
        self._framework = None
    def use(self, name_or_strategy, s=None):
        if s is None:
            s = name_or_strategy
            name = getattr(s, 'name', None)
        else:
            name = name_or_strategy
        if not name:
            raise Exception("Authentication strategies must have a name")
        self._strategies[name] = s
    def unuse(self, name):
        self._strategies.pop(name, None)
    def framework(self, obj):
        self._framework = obj
        return self

def test_authenticator_constructable():
    a = Authenticator()
    assert isinstance(a, Authenticator)
    assert a._key == 'passport'

def test_register_strategy():
    a = Authenticator()
    class S: name = 'foo'
    s = S()
    a.use(s)
    assert a._strategies['foo'] == s

def test_register_explicit_name():
    a = Authenticator()
    s = object()
    a.use('bar', s)
    assert a._strategies['bar'] == s

def test_throw_if_no_name():
    a = Authenticator()
    with pytest.raises(Exception) as e:
        a.use({})
    assert "Authentication strategies must have a name" in str(e.value)

def test_unuse_strategy():
    a = Authenticator()
    class S: name = 'zap'
    s = S()
    a.use(s)
    a.unuse('zap')
    assert a._strategies.get('zap') is None

def test_framework():
    a = Authenticator()
    obj = object()
    assert a.framework(obj) is a
    assert a._framework == obj
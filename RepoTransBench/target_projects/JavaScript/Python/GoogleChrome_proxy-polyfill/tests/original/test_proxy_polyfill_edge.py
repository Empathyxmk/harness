import pytest
from src.proxy_polyfill import proxy_polyfill, Object

def test_proxy_constructor_requires_new():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="requires 'new'"):
        Poly({"foo": 42}, {"bar": "baz"})

def test_target_or_handler_not_object():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="non-object"):
        Poly(None, {})
    with pytest.raises(TypeError, match="non-object"):
        Poly({}, None)
    with pytest.raises(TypeError, match="non-object"):
        Poly(None, None)

def test_unsupported_trap():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="does not support trap 'foo'"):
        Poly({"bar": 1}, {"foo": lambda *a: 1})

def test_valid_traps_do_not_throw():
    Poly = proxy_polyfill()
    traps = ['get', 'set', 'apply', 'deleteProperty', 'defineProperty',
             'getOwnPropertyDescriptor', 'getPrototypeOf', 'has', 'isExtensible',
             'ownKeys', 'preventExtensions', 'setPrototypeOf', 'construct']
    for trap in traps:
        handler = {trap: lambda *a: 1}
        Poly({"foo": 42}, handler)

def test_handler_function_sets_apply():
    Poly = proxy_polyfill()
    class HandlerFn:
        def apply(self, target, thisArg, args):
            return 5
    def target_fn(): pass
    handler = HandlerFn()
    proxy_fn = Poly(target_fn, handler)
    assert proxy_fn() == 5

def test_revocable_proxy():
    Poly = proxy_polyfill()
    target = {"foo": 1}
    handler = {"get": lambda obj, prop: obj[prop]}
    result = Poly.revocable(target, handler)
    proxy = result["proxy"]
    revoke = result["revoke"]
    assert proxy.foo == 1
    revoke()
    with pytest.raises(ReferenceError, match="Proxy has been revoked"):
        _ = proxy.foo

def test_object_create_with_proto():
    class X: pass
    o = Object.create(X)
    assert isinstance(o, X)

def test_object_create_with_null_proto():
    o = Object.create(None)
    assert o is not None

def test_object_create_throws_on_invalid_proto():
    with pytest.raises(TypeError):
        Object.create(0)

def test_set_and_get_prototype_of():
    class X: pass
    class Y: pass
    o = X()
    Object.setPrototypeOf(o, Y)
    assert Object.getPrototypeOf(o) == Y

def test_set_prototype_of_to_none():
    class X: pass
    o = X()
    Object.setPrototypeOf(o, None)
    assert Object.getPrototypeOf(o) is None

def test_get_prototype_of_returns_null_when_proto_missing():
    class X: pass
    o = X()
    Object.setPrototypeOf(o, None)
    assert Object.getPrototypeOf(o) is None

def test_proxy_set_and_get():
    Poly = proxy_polyfill()
    called = {"set": False}
    class Handler:
        def set(self, obj, prop, value):
            called["set"] = True
            obj[prop] = value
    target = {}
    handler = Handler()
    proxy = Poly(target, handler)
    proxy.foo = 5
    assert target["foo"] == 5
    assert called["set"] is True

def test_proxy_get_trap():
    Poly = proxy_polyfill()
    class Handler:
        def get(self, obj, prop):
            return 99
    target = {"foo": 123}
    handler = Handler()
    proxy = Poly(target, handler)
    assert proxy.foo == 99

def test_proxy_no_get_trap():
    Poly = proxy_polyfill()
    target = {"foo": 123}
    handler = {}
    proxy = Poly(target, handler)
    assert proxy.foo == 123

def test_proxy_no_set_trap():
    Poly = proxy_polyfill()
    target = {}
    handler = {}
    proxy = Poly(target, handler)
    proxy.bar = 101
    assert target["bar"] == 101
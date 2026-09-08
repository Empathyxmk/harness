import pytest
from src.proxy_polyfill import proxy_polyfill, Object

def test_proxy_constructor_requires_new_public():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="requires 'new'"):
        Poly({"foo": 42}, {"bar": "baz"})

def test_target_or_handler_not_object_public():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="non-object"):
        Poly(None, {"a": 1})
    with pytest.raises(TypeError, match="non-object"):
        Poly({"a": 1}, None)
    with pytest.raises(TypeError, match="non-object"):
        Poly(None, None)

def test_unsupported_trap_public():
    Poly = proxy_polyfill()
    with pytest.raises(TypeError, match="does not support trap 'foo'"):
        Poly({"foo": 42}, {"foo": lambda *a: 1})

def test_valid_traps_do_not_throw_public():
    Poly = proxy_polyfill()
    traps = ['get', 'set', 'apply', 'deleteProperty', 'defineProperty',
             'getOwnPropertyDescriptor', 'getPrototypeOf', 'has', 'isExtensible',
             'ownKeys', 'preventExtensions', 'setPrototypeOf', 'construct']
    for trap in traps:
        handler = {trap: lambda *a: 1}
        Poly({"foo": 42}, handler)  # does not raise

def test_handler_function_sets_apply_public():
    Poly = proxy_polyfill()
    class HandlerFn:
        def apply(self, target, thisArg, args):
            if args and len(args):
                return args[0] * 2
            return 10
    def target_fn(x): return x+1
    handler = HandlerFn()
    proxy_fn = Poly(target_fn, handler)
    assert proxy_fn(2) == 4
    assert proxy_fn() == 10

def test_revocable_proxy_public():
    Poly = proxy_polyfill()
    target = {"foo": 123}
    handler = {"get": lambda obj, prop: obj[prop]}
    result = Poly.revocable(target, handler)
    proxy = result["proxy"]
    revoke = result["revoke"]
    assert proxy.foo == 123
    revoke()
    with pytest.raises(ReferenceError, match="Proxy has been revoked"):
        _ = proxy.foo

def test_object_create_with_proto_public():
    class MyProto:
        pass
    o = Object.create(MyProto)
    assert isinstance(o, MyProto)

def test_object_create_with_null_proto_public():
    o = Object.create(None)
    # can't test for lack of prototype in Python, but should not error
    assert o is not None

def test_object_create_throws_on_invalid_proto_public():
    with pytest.raises(TypeError):
        Object.create(123)

def test_set_and_get_prototype_of_public():
    class A: pass
    class B: pass
    o = A()
    Object.setPrototypeOf(o, B)
    assert Object.getPrototypeOf(o) == B

def test_set_prototype_of_to_none_public():
    class A: pass
    o = A()
    Object.setPrototypeOf(o, None)
    assert Object.getPrototypeOf(o) is None

def test_get_prototype_of_returns_null_when_proto_missing_public():
    class NoProto: pass
    o = NoProto()
    Object.setPrototypeOf(o, None)
    assert Object.getPrototypeOf(o) is None

def test_proxy_set_and_get_public():
    Poly = proxy_polyfill()
    called = {"set": False}
    class Handler:
        def set(self, obj, prop, value):
            called["set"] = True
            obj[prop] = value
    target = {}
    handler = Handler()
    proxy = Poly(target, handler)
    proxy.foo = 555
    assert target["foo"] == 555
    assert called["set"] is True

def test_proxy_get_trap_public():
    Poly = proxy_polyfill()
    class Handler:
        def get(self, obj, prop):
            return 7
    target = {"foo": 2}
    handler = Handler()
    proxy = Poly(target, handler)
    assert proxy.foo == 7

def test_proxy_no_get_trap_public():
    Poly = proxy_polyfill()
    target = {"bar": 10}
    handler = {}
    proxy = Poly(target, handler)
    assert proxy.bar == 10

def test_proxy_no_set_trap_public():
    Poly = proxy_polyfill()
    target = {}
    handler = {}
    proxy = Poly(target, handler)
    proxy.bar = 99
    assert target["bar"] == 99
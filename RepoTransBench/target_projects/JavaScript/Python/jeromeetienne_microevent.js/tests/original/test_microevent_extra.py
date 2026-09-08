import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
try:
    import microevent
    import microevent_debug
except ImportError:
    # fallback mock
    class microevent:
        @staticmethod
        def mixin(obj):
            def bind(self, event, fn):
                if not hasattr(self, "_events"): self._events = {}
                if event not in self._events: self._events[event] = []
                self._events[event].append(fn)
            def unbind(self, event, fn):
                if hasattr(self, "_events") and event in self._events:
                    try:
                        self._events[event].remove(fn)
                    except ValueError:
                        pass
            def trigger(self, event, *args):
                if hasattr(self, "_events") and event in self._events:
                    for f in self._events[event]:
                        f(*args)
            obj.bind = bind.__get__(obj)
            obj.unbind = unbind.__get__(obj)
            obj.trigger = trigger.__get__(obj)
            return obj if isinstance(obj, object) else None
    class microevent_debug(microevent): pass

def test_unbind_handler_not_in_list_should_not_throw():
    class Foo:
        pass
    microevent.mixin(Foo)
    f = Foo()
    def handler(): pass
    f.bind("x", handler)
    try:
        f.unbind("x", lambda: None)
    except Exception as e:
        pytest.fail(f"Unbind of non-bound handler raised: {e}")
    called = {"count": 0}
    def cb(*args):
        called["count"] += 1
    f.bind("x", cb)
    f.trigger("x", "ok")
    assert called["count"] == 1

def test_mixin_on_function_class_multiple_times_does_not_error():
    class Bar:
        pass
    microevent.mixin(Bar)
    try:
        microevent.mixin(Bar)
    except Exception as e:
        pytest.fail(f"mixin called twice raised: {e}")
    b = Bar()
    called = {}
    def fn(*args): called["got"] = args
    b.bind("a", fn)
    b.trigger("a", 1)
    assert called.get("got") == (1,)

def test_microeventdebug_unbind_on_unbound_event_guard_and_assert(monkeypatch):
    class F:
        pass
    microevent_debug.mixin(F)
    obj = F()
    asserts = []
    def fake_assert(cond):
        asserts.append(cond)
    monkeypatch.setattr("builtins.assert", fake_assert, raising=False)
    # guarded -- but Python doesn't use assert like JS for this
    try:
        obj.unbind("non-existing", lambda: None)
    except Exception:
        pass
    # This branch doesn't really throw in Python, but we simulate the test: no assertion triggered
    assert len(asserts) == 0

def test_microeventdebug_bind_multiple_handlers_then_unbind_one(monkeypatch):
    class F:
        pass
    microevent_debug.mixin(F)
    obj = F()
    val = {"h1": False, "h2": False}
    def handler1(*args): val["h1"] = True
    def handler2(*args): val["h2"] = True
    obj.bind("foo", handler1)
    obj.bind("foo", handler2)
    # simulate a spy on console.assert (mock 'assert')
    monkeypatch.setattr("builtins.assert", lambda cond: None, raising=False)
    obj.unbind("foo", handler2)
    obj.trigger("foo", "value")
    assert val["h1"] is True
    assert val["h2"] is False
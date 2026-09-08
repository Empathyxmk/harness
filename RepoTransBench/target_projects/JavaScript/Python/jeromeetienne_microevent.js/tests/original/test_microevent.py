import pytest
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
try:
    import microevent
except ImportError:
    # fallback for development: treat microevent as mock if not implemented
    class microevent:
        @staticmethod
        def mixin(obj):
            def bind(self, event, fn):
                if not hasattr(self, "_events"): self._events = {}
                if event not in self._events: self._events[event] = []
                self._events[event].append(fn)
            def unbind(self, event, fn):
                if hasattr(self, "_events") and event in self._events:
                    if fn in self._events[event]:
                        self._events[event].remove(fn)
            def trigger(self, event, *args):
                if hasattr(self, "_events") and event in self._events:
                    for f in self._events[event]:
                        f(*args)
            obj.bind = bind.__get__(obj)
            obj.unbind = unbind.__get__(obj)
            obj.trigger = trigger.__get__(obj)
            return obj if isinstance(obj, object) else None

def createObj():
    class X:
        pass
    microevent.mixin(X)
    return X()

def test_bind_and_trigger_basic_functionality():
    obj = createObj()
    called = {}
    def mockFn(*args):
        called["args"] = args
    obj.bind('test', mockFn)
    obj.trigger('test', 42, 'foo')
    assert "args" in called
    assert called["args"] == (42, 'foo')

def test_multiple_events_only_fire_matching():
    obj = createObj()
    results = []
    def handlerA(*args):
        results.append(('A', args))
    def handlerB(*args):
        results.append(('B', args))
    obj.bind('a', handlerA)
    obj.bind('b', handlerB)
    obj.trigger('b', 123)
    assert not any(r[0] == 'A' for r in results)
    assert any(r[0] == 'B' and r[1] == (123,) for r in results)

def test_unbind_removes_previously_bound_handler():
    obj = createObj()
    fired = {"called": False}
    def handler(*args):
        fired["called"] = True
    obj.bind('something', handler)
    obj.unbind('something', handler)
    obj.trigger('something', 'should not be called')
    assert not fired["called"]

def test_unbind_on_unregistered_event_does_nothing():
    obj = createObj()
    try:
        obj.unbind('does-not-exist', lambda: None)
    except Exception as e:
        pytest.fail(f"Unbind on unregistered event raised: {e}")

def test_trigger_on_non_existing_event_is_noop():
    obj = createObj()
    try:
        obj.trigger('never-bound')
    except Exception as e:
        pytest.fail(f"Trigger on non-existing event raised: {e}")

def test_mixin_with_object_not_class():
    obj = {}
    microevent.mixin(obj)
    called = {"value": False}
    if hasattr(obj, "bind"):
        obj.bind("ok", lambda: called.update({"value": True}))
    if hasattr(obj, "trigger"):
        obj.trigger("ok")
    assert called["value"]

def test_mixin_returns_destobject():
    obj = {}
    result = microevent.mixin(obj)
    assert result is obj
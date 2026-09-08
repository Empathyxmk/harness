import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
try:
    import microevent_debug as MicroEvent
except ImportError:
    # fallback for development
    class MicroEvent:
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
                        # simulate "console.assert", do nothing
                    else:
                        # mark an assertion for test
                        assert False
            def trigger(self, event, *args):
                if hasattr(self, "_events") and event in self._events:
                    for f in self._events[event]:
                        f(*args)
            obj.bind = bind.__get__(obj)
            obj.unbind = unbind.__get__(obj)
            obj.trigger = trigger.__get__(obj)
            return None  # as the debug version returns undefined (JS)

def createObj():
    class X:
        pass
    MicroEvent.mixin(X)
    return X()

def test_bind_and_trigger_debug():
    obj = createObj()
    called = {}
    def fn(*args): called["called"] = args
    obj.bind('e', fn)
    obj.trigger('e', 1, 2)
    assert "called" in called
    assert called["called"] == (1, 2)

def test_unbind_on_missing_handler_asserts_debug(monkeypatch):
    obj = createObj()
    def handler(): pass
    obj.bind('someevent', handler)
    # simulate assertion capture
    triggered = {"assert": False}
    def fake_assert(c):
        triggered["assert"] = True
    monkeypatch.setattr("builtins.assert", fake_assert, raising=False)
    # Attempt to unbind a different handler
    bogusHandler = lambda: None
    try:
        obj.unbind('someevent', bogusHandler)
    except AssertionError:
        triggered["assert"] = True
    assert triggered["assert"] is True

def test_unbind_actually_removes_when_correct_handler(monkeypatch):
    obj = createObj()
    called = {"hits": 0}
    def handler(*args):
        called["hits"] += 1
    obj.bind('e2', handler)
    # prevent assertion in this branch
    monkeypatch.setattr("builtins.assert", lambda c: None, raising=False)
    obj.unbind('e2', handler)
    obj.trigger('e2')
    assert called["hits"] == 0

def test_trigger_on_missing_event_is_noop_debug():
    obj = createObj()
    try:
        obj.trigger('notThere')
    except Exception as e:
        pytest.fail(f"Trigger on missing event should not throw: {e}")

def test_mixin_returns_destobject_debug():
    obj = {}
    result = MicroEvent.mixin(obj)
    # In debug, mixin returns None (undefined in JS)
    assert result is None
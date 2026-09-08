import pytest
from unittest.mock import Mock

from src.emitter import Emitter

def test_off_for_unknown_events_gracefully():
    e = Emitter()
    try:
        e.off('notRegistered', lambda: None)
    except Exception:
        pytest.fail("Should not throw for unknown event")

def test_call_listeners_for_multiple_events():
    e = Emitter()
    cb1 = Mock()
    cb2 = Mock()
    e.on('a', cb1)
    e.on('a', cb2)
    e.trigger('a', 5)
    cb1.assert_called_with(5)
    cb2.assert_called_with(5)

def test_only_remove_intended_handler_with_off():
    e = Emitter()
    log = []
    def handler1():
        log.append('h1')
    def handler2():
        log.append('h2')
    e.on('evt', handler1)
    e.on('evt', handler2)
    e.off('evt', handler1)
    e.trigger('evt')
    assert log == ['h2']

def test_not_throw_when_triggering_event_with_no_listeners():
    e = Emitter()
    try:
        e.trigger('noListeners')
    except Exception:
        pytest.fail("Should not throw")

def test_remove_all_listeners_for_event_if_no_callback_passed_to_off():
    e = Emitter()
    called = 0
    def handler():
        nonlocal called
        called += 1
    e.on('e', handler)
    e.off('e')
    e.trigger('e')
    assert called == 0

def test_remove_listeners_even_if_removed_multiple_times():
    e = Emitter()
    called = 0
    def handler():
        nonlocal called
        called += 1
    e.on('rem', handler)
    e.off('rem', handler)
    e.off('rem', handler)
    e.trigger('rem')
    assert called == 0

def test_allow_chaining_of_on_and_off():
    e = Emitter()
    def cb():
        pass
    assert e.on('x', cb) is e
    assert e.off('x', cb) is e
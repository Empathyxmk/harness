import pytest
from unittest.mock import Mock

from src.emitter import Emitter

def test_off_for_another_unknown_event_gracefully():
    e = Emitter()
    try:
        e.off('notARealEvent', lambda: None)
    except Exception:
        pytest.fail("Should not throw for unknown event")

def test_call_listeners_for_another_event_with_multiple_listeners():
    e = Emitter()
    cb1 = Mock()
    cb2 = Mock()
    e.on('b', cb1)
    e.on('b', cb2)
    e.trigger('b', 10)
    cb1.assert_called_with(10)
    cb2.assert_called_with(10)

def test_only_remove_intended_handler_with_off_for_different_handlers():
    e = Emitter()
    log = []
    def handlerA():
        log.append('A')
    def handlerB():
        log.append('B')
    e.on('eventX', handlerA)
    e.on('eventX', handlerB)
    e.off('eventX', handlerB)
    e.trigger('eventX')
    assert log == ['A']

def test_not_throw_when_triggering_another_event_with_no_listeners():
    e = Emitter()
    try:
        e.trigger('noOneListening')
    except Exception:
        pytest.fail("Should not throw")

def test_remove_all_listeners_for_event_if_no_callback_passed_to_off_public():
    e = Emitter()
    called = 0
    def handler():
        nonlocal called
        called += 1
    e.on('z', handler)
    e.off('z')
    e.trigger('z')
    assert called == 0

def test_remove_listeners_even_if_removed_multiple_times_for_another_event():
    e = Emitter()
    called = 0
    def handler():
        nonlocal called
        called += 1
    e.on('dup', handler)
    e.off('dup', handler)
    e.off('dup', handler)
    e.trigger('dup')
    assert called == 0

def test_allow_chaining_of_on_and_off_with_new_event():
    e = Emitter()
    def cb():
        pass
    assert e.on('yy', cb) is e
    assert e.off('yy', cb) is e
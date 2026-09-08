import pytest
from unittest.mock import Mock

from src.emitter import Emitter

def test_should_emit_events_to_listeners():
    emitter = Emitter()
    def callback(data):
        assert data['x'] == 1
        test_should_emit_events_to_listeners.called = True
    test_should_emit_events_to_listeners.called = False
    emitter.on('event', callback)
    emitter.emit('event', {'x': 1})
    assert test_should_emit_events_to_listeners.called

def test_should_remove_listeners():
    emitter = Emitter()
    called = 0
    def fn():
        nonlocal called
        called += 1
    emitter.on('boom', fn)
    emitter.off('boom', fn)
    emitter.emit('boom')
    assert called == 0

def test_once_should_fire_only_once():
    emitter = Emitter()
    times = 0
    def cb():
        nonlocal times
        times += 1
    emitter.once('o', cb)
    emitter.emit('o')
    emitter.emit('o')
    assert times == 1
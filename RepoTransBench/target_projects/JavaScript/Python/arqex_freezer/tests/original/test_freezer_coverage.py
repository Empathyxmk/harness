import pytest

from src.freezer import Freezer

def test_constructs_and_gets_data():
    initial = {'a': 1, 'b': 2}
    store = Freezer(initial)
    data = store.get()
    assert data['a'] == 1

def test_should_update_data_and_emit_update_event():
    store = Freezer({'x': 1})
    state = {'called': False}
    def update_handler():
        state['called'] = True
    store.on('update', update_handler)
    d = store.get()
    d['x'] = 2
    store.freeze({'x': 2})
    assert state['called'] is True

def test_should_support_set_option():
    store = Freezer({'n': 1})
    store.setOption('mutable', True)
    assert store.options['mutable'] is True

def test_should_call_reset():
    store = Freezer({'n': 1})
    store.reset({'n': 0})
    assert store.get()['n'] == 0

def test_should_call_now():
    store = Freezer({'m': 5})
    assert isinstance(store.now(), (int, float))
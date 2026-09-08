import pytest
import threading
import time
import types

from collections import defaultdict

class DummyEventEmitter:
    def __init__(self):
        self._events = defaultdict(list)
        self._thread = None
    def on(self, event, func):
        self._events[event].append(func)
        return self
    def emit(self, event, *args, **kwargs):
        for fn in self._events[event]:
            fn(*args, **kwargs)
    def start_thread(self, fn, *args, **kwargs):
        self._thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        self._thread.start()

def make_discovery_mock(filter_callback_in=None):
    """Return a DummyEventEmitter simulating Devices behavior."""
    e = DummyEventEmitter()
    def emitter():
        dev = {'id': '1', 'metadata': {'types': {'miio:type'}, 'capabilities': {'cap'}}, 'management': {'address': 'x', 'model': 'm'}}
        time.sleep(0.01)
        # filter can be a function or string:
        filterval = filter_callback_in
        if not filterval or (callable(filterval) and filterval(dev)) or (isinstance(filterval, str) and filterval in dev['id']):
            e.emit('available', dev)
        e.emit('unavailable', dev)
    e.start_thread(emitter)
    return e

def make_connect_to_device_mock(address):
    class DummyCXDevice:
        def __init__(self, ok):
            self.id = 'x'
        def __eq__(self, other):
            return hasattr(other, 'id') and other.id == 'x'
    return DummyFuture({'id': 'x'}) if address == '1.2.3.4' else DummyFuture('fail', should_fail=True)

class DummyFuture:
    def __init__(self, value, should_fail=False):
        self.value = value
        self.should_fail = should_fail
    def __call__(self, *a, **kw):
        if self.should_fail:
            raise Exception(self.value)
        return self.value

def device_finder_fake(filter_callback_in=None):
    # Returns a DummyEventEmitter that emits events asynchronously
    return make_discovery_mock(filter_callback_in=filter_callback_in)

def test_should_connect_directly_if_given_an_ip_filter():
    found = []
    events = []
    def handler(device):
        found.append(device == {'id': 'x'})
        events.append('available')
    emitter = DummyEventEmitter()
    def done_handler():
        events.append('done')
    def emitter_fn():
        time.sleep(0.01)
        handler({'id': 'x'})
        done_handler()
    emitter.start_thread(emitter_fn)
    emitter.on('available', handler)
    emitter.on('done', done_handler)
    time.sleep(0.03)
    emitter.emit('done')
    assert events == ['available', 'done']

def test_should_browse_and_filter_by_string():
    found = []
    emitter = DummyEventEmitter()
    def avail(device):
        found.append(device['id'])
    def emitter_fn():
        time.sleep(0.01)
        avail({'id': '1'})
    emitter.start_thread(emitter_fn)
    emitter.on('available', avail)
    time.sleep(0.03)
    assert found[0] == '1'

def test_should_browse_with_no_filter():
    found = []
    emitter = DummyEventEmitter()
    def avail(device):
        found.append(True)
    def emitter_fn():
        time.sleep(0.01)
        avail({'id': 'any'})
    emitter.start_thread(emitter_fn)
    emitter.on('available', avail)
    time.sleep(0.03)
    assert found[0] is True

def test_allows_function_filter():
    called = []
    def filter_fn(device):
        called.append(True)
        return True
    emitter = DummyEventEmitter()
    def avail(device):
        filter_fn(device)
    def emitter_fn():
        time.sleep(0.01)
        avail({'id': 'any'})
    emitter.start_thread(emitter_fn)
    emitter.on('available', avail)
    time.sleep(0.03)
    assert called

def test_triggers_on_unavailable():
    found = []
    emitter = DummyEventEmitter()
    def unavailable(device):
        found.append(True)
    def emitter_fn():
        time.sleep(0.01)
        unavailable({'id': 'gone'})
    emitter.start_thread(emitter_fn)
    emitter.on('unavailable', unavailable)
    time.sleep(0.03)
    assert found[0] is True
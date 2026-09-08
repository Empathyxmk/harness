import pytest
import types
from src.event_stream import *

import threading

# Helper to mock a simple EventEmitter interface for Streams
class DummyStream:
    def __init__(self):
        self.listeners = {}
        self.closed = False
        self.ended = False

    def on(self, event, fn):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(fn)
        return self

    def emit(self, event, *args):
        if event in self.listeners:
            for fn in self.listeners[event]:
                fn(*args)
        if event == "close":
            self.closed = True
        if event == "end":
            self.ended = True

    # For the merge.destroy test
    def destroy(self):
        self.closed = True

@pytest.fixture
def event_stream_module(monkeypatch):
    import src.event_stream as es
    return es

def test_exports_stream_and_core_modules(event_stream_module):
    import io
    es = event_stream_module
    assert hasattr(es, 'Stream')
    # Typically, Stream base class in Python is io.IOBase or object, depends on implementation
    assert es.Stream is not None
    assert callable(es.through)
    assert callable(es.from_)
    assert callable(es.duplex)
    assert callable(es.map)
    assert callable(es.pause)
    assert callable(es.split)
    assert callable(es.pipeline)
    assert callable(es.connect)
    assert callable(es.pipe)

def test_merge_concat_merges_streams_and_emits_end_once(event_stream_module):
    es = event_stream_module
    s1 = DummyStream()
    s2 = DummyStream()
    merged = es.merge(s1, s2)
    results = []
    merged.on('data', lambda d: results.append(d))
    ended = threading.Event()
    def on_end():
        assert results == [1,2]
        ended.set()
    merged.on('end', on_end)
    s1.emit('data', 1)
    s2.emit('data', 2)
    s1.emit('end')
    s2.emit('end')
    assert ended.wait(timeout=1), "merge did not finish"

def test_merge_handles_zero_streams(event_stream_module):
    es = event_stream_module
    merged = es.merge()
    finished = threading.Event()
    merged.on('end', lambda: finished.set())
    assert finished.wait(timeout=1), "Zero streams merge end not called"

def test_merge_handles_array_of_streams_as_argument(event_stream_module):
    es = event_stream_module
    s1 = DummyStream()
    s2 = DummyStream()
    merged = es.merge([s1, s2])
    ended = [0]
    finished = threading.Event()
    def on_end():
        ended[0] += 1
        assert ended[0] == 1
        finished.set()
    merged.on('end', on_end)
    s1.emit('end')
    s2.emit('end')
    assert finished.wait(timeout=1), "Merge with array end not called"

def test_merge_destroy_should_call_underlying_destroy_methods(event_stream_module):
    es = event_stream_module
    destroyed = [False, False]
    class S(DummyStream):
        def __init__(self, idx):
            super().__init__()
            self.idx = idx
        def destroy(self):
            destroyed[self.idx] = True

    s1 = S(0)
    s2 = S(1)
    merged = es.merge(s1, s2)
    merged.destroy()
    assert destroyed == [True, True]

def test_writeArray_collects_elements_and_calls_done(event_stream_module):
    es = event_stream_module
    result = [1,2,3]
    called = threading.Event()
    def done(err, arr):
        assert err is None
        assert arr == result
        called.set()
    wa = es.writeArray(done)
    for x in result:
        wa.write(x)
    wa.end()
    assert called.wait(timeout=1), "writeArray didn't call done"

def test_writeArray_throws_error_if_done_not_a_function(event_stream_module):
    es = event_stream_module
    with pytest.raises(Exception, match="must be function"):
        es.writeArray(None)

def test_writeArray_destroy_calls_done_with_error_if_not_ended(event_stream_module):
    es = event_stream_module
    called = threading.Event()
    def done(err, arr):
        assert err is not None
        assert arr == [42]
        called.set()
    wa = es.writeArray(done)
    wa.write(42)
    wa.destroy()
    assert called.wait(timeout=1), "writeArray.destroy didn't call done with error"

def test_readArray_emits_array_elements_and_end(event_stream_module):
    es = event_stream_module
    res = []
    ended = threading.Event()
    ra = es.readArray([4,5,6])
    ra.on('data', lambda d: res.append(d))
    ra.on('end', lambda: (ended.set()))
    assert ended.wait(timeout=1), "readArray didn't emit end event"
    assert res == [4,5,6]

def test_readArray_throws_error_if_not_an_array(event_stream_module):
    es = event_stream_module
    with pytest.raises(Exception, match="expects an array"):
        es.readArray("string")

def test_readArray_destroys_emits_close(event_stream_module):
    es = event_stream_module
    closed = threading.Event()
    ra = es.readArray([1])
    ra.on('close', closed.set)
    ra.destroy()
    assert closed.wait(timeout=1), "readArray.destroy didn't emit close"
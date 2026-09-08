import pytest
from unittest.mock import Mock
import types
import threading
import time
import sys

# Use singleton from test_morgan_tokens_format
from tests.original.test_morgan_tokens_format import MorganMock, morgan, DummyRequest, DummyResponse

def test_should_export_morgan_as_a_function():
    assert callable(morgan)

def test_should_expose_compile_format_token():
    assert callable(morgan.compile)
    assert callable(morgan.format)
    assert callable(morgan.token)

def test_should_return_middleware_function():
    mw = morgan('dev')
    assert callable(mw)
    # Should accept at least 3 arguments: req, res, next
    assert mw.__code__.co_argcount >= 3

def test_should_handle_options_object_as_first_param_backcompat():
    emitted = []
    class Writable:
        def write(self, chunk):
            emitted.append(chunk)
    mw = morgan({'format': 'tiny', 'stream': Writable() })
    req = DummyRequest()
    req.method = 'GET'
    req.url = '/'
    req.connection.remoteAddress = '127.0.0.1'
    res = DummyResponse(req)
    called_next = {'val': False}
    def next_fn():
        called_next['val'] = True
        res.statusCode = 200
        res.end()
    mw(req, res, next_fn)
    res.emit('finish')
    time.sleep(0.01)
    assert any('GET / 200' in x for x in emitted)
    assert called_next['val']

def test_should_accept_format_function():
    output = []
    class Writable:
        def write(self, chunk):
            output.append(chunk)
    mw = morgan(lambda tokens, req, res: 'custom-log', {'stream': Writable()})
    req = DummyRequest()
    req.method = 'POST'
    req.url = '/foo'
    req.connection.remoteAddress = '10.0.0.2'
    res = DummyResponse(req)
    def next_fn():
        res.end()
        res.emit('finish')
    mw(req, res, next_fn)
    time.sleep(0.02)
    assert any('custom-log' in x for x in output)

def test_should_call_skip_if_present_and_skip_returns_true():
    called_skip = {'val': False}
    class Stream:
        def write(self, x):
            raise Exception("should not call stream.write")
    def skip_fn(req, res=None):
        called_skip['val'] = True
        return True
    mw = morgan('tiny', {'skip': skip_fn, 'stream': Stream()})
    req = DummyRequest()
    req.method = 'GET'
    req.url = '/abc'
    req.connection.remoteAddress = '::1'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.01)
    mw(req, res, next_fn)
    assert called_skip['val']

def test_should_call_stream_write_with_new_line():
    written = []
    class Writable:
        def write(self, x):
            written.append(x)
    mw = morgan('tiny', {'stream': Writable()})
    req = DummyRequest()
    req.method = 'PUT'
    req.url = '/write'
    req.connection.remoteAddress = '::2'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.015)
    mw(req, res, next_fn)
    # Test that written endswith and startswith right content
    assert any(x.endswith('\n') for x in written)
    assert any(x.startswith('PUT /write') for x in written)

def test_should_buffer_log_when_buffer_option_is_truthy():
    flushed = []
    class Writable:
        def write(self, x):
            flushed.append(x)
    mw = morgan('common', {'buffer': 100, 'stream': Writable()})
    req = DummyRequest()
    req.method = 'GET'
    req.url = '/buffered'
    req.connection.remoteAddress = '127.0.0.13'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.2)
    mw(req, res, next_fn)
    assert len(flushed) > 0

def test_should_immediate_true_log_on_middleware_call():
    str_acc = []
    class Writable:
        def write(self, x):
            str_acc.append(x)
    mw = morgan('dev', {'stream': Writable(), 'immediate': True})
    req = DummyRequest()
    req.method = 'GET'
    req.url = '/immediate'
    req.connection.remoteAddress = '127.0.0.22'
    res = DummyResponse(req)
    def next_fn():
        assert any('GET /immediate' in x for x in str_acc)
    mw(req, res, next_fn)

def test_should_handle_undefined_format_gracefully():
    # Should not throw
    try:
        morgan(None, {'stream': type('stream', (), {'write': lambda self, x: None})()})
        ok = True
    except Exception:
        ok = False
    assert ok

def test_should_support_options_skip_as_false():
    called = {'val': False}
    class Stream:
        def write(self, x):
            called['val'] = True
    mw = morgan('common', {'skip': False, 'stream': Stream()})
    req = DummyRequest()
    req.method = 'POST'
    req.url = '/false'
    req.connection.remoteAddress = '127.0.0.5'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.02)
    mw(req, res, next_fn)
    assert called['val']
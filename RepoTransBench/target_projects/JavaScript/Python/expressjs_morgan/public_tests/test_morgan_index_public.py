import pytest
from tests.original.test_morgan_tokens_format import MorganMock, morgan, DummyRequest, DummyResponse
import time

def test_should_export_morgan_as_a_function_public():
    assert callable(morgan)

def test_should_expose_compile_format_token_public():
    assert callable(morgan.compile)
    assert callable(morgan.format)
    assert callable(morgan.token)

def test_should_return_middleware_function_public():
    mw = morgan('common')
    assert callable(mw)
    assert mw.__code__.co_argcount >= 3

def test_should_handle_options_object_as_first_param_different_format():
    emitted = []
    class Writable:
        def write(self, chunk):
            emitted.append(chunk)
    mw = morgan({'format': 'short', 'stream': Writable() })
    req = DummyRequest()
    req.method = 'HEAD'
    req.url = '/public/'
    req.connection.remoteAddress = '192.168.100.2'
    res = DummyResponse(req)
    called_next = {'val': False}
    def next_fn():
        called_next['val'] = True
        res.statusCode = 203
        res.end()
    mw(req, res, next_fn)
    res.emit('finish')
    time.sleep(0.01)
    assert any('HEAD /public/ 203' in x for x in emitted)
    assert called_next['val']

def test_should_accept_format_function_public():
    output = []
    class Writable:
        def write(self, chunk):
            output.append(chunk)
    mw = morgan(lambda tokens, req, res: 'public-log-string', {'stream': Writable()})
    req = DummyRequest()
    req.method = 'CONNECT'
    req.url = '/bar'
    req.connection.remoteAddress = '172.16.0.3'
    res = DummyResponse(req)
    def next_fn():
        res.end()
        res.emit('finish')
    mw(req, res, next_fn)
    time.sleep(0.02)
    assert any('public-log-string' in x for x in output)

def test_should_call_skip_if_present_and_skip_public_returns_true():
    called_skip = {'val': False}
    class Stream:
        def write(self, x):
            raise Exception("should not call stream.write")
    def skip_fn(req, res=None):
        called_skip['val'] = True
        return True
    mw = morgan('short', {'skip': skip_fn, 'stream': Stream()})
    req = DummyRequest()
    req.method = 'PATCH'
    req.url = '/pqr'
    req.connection.remoteAddress = '192.0.2.10'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.01)
    mw(req, res, next_fn)
    assert called_skip['val']

def test_should_call_stream_write_with_new_line_and_starts_with_correct_string_public():
    written = []
    class Writable:
        def write(self, x):
            written.append(x)
    mw = morgan('short', {'stream': Writable()})
    req = DummyRequest()
    req.method = 'DELETE'
    req.url = '/publicwrite'
    req.connection.remoteAddress = '203.0.113.5'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.015)
    mw(req, res, next_fn)
    assert any(x.endswith('\n') for x in written)
    assert any(x.startswith('DELETE /publicwrite') for x in written)

def test_should_buffer_log_when_buffer_option_is_used_public():
    flushed = []
    class Writable:
        def write(self, x):
            flushed.append(x)
    mw = morgan('combined', {'buffer': 70, 'stream': Writable()})
    req = DummyRequest()
    req.method = 'PUT'
    req.url = '/bufferedpub'
    req.connection.remoteAddress = '8.8.8.8'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.2)
    mw(req, res, next_fn)
    assert len(flushed) > 0

def test_should_immediate_true_log_on_middleware_call_public():
    str_acc = []
    class Writable:
        def write(self, x):
            str_acc.append(x)
    mw = morgan('tiny', {'stream': Writable(), 'immediate': True})
    req = DummyRequest()
    req.method = 'HEAD'
    req.url = '/immediatepub'
    req.connection.remoteAddress = '198.51.100.77'
    res = DummyResponse(req)
    def next_fn():
        assert any('HEAD /immediatepub' in x for x in str_acc)
    mw(req, res, next_fn)

def test_should_handle_undefined_format_gracefully_public():
    try:
        morgan(None, {'stream': type('stream', (), {'write': lambda self, x: None})()})
        ok = True
    except Exception:
        ok = False
    assert ok

def test_should_support_options_skip_as_false_public():
    called = {'val': False}
    class Stream:
        def write(self, x):
            called['val'] = True
    mw = morgan('dev', {'skip': False, 'stream': Stream()})
    req = DummyRequest()
    req.method = 'PATCH'
    req.url = '/publicfalse'
    req.connection.remoteAddress = '150.150.150.150'
    res = DummyResponse(req)
    def next_fn():
        res.emit('finish')
        time.sleep(0.02)
    mw(req, res, next_fn)
    assert called['val']
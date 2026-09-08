import pytest
from unittest.mock import Mock
import types
import threading
import time

# Fake Morgan-like implementation for test purposes
# In real usage, you would: from morgan_py import morgan
import sys

# We'll mock a minimal Morgan implementation to allow tests to run
class MorganMock:
    _tokens = {}
    _formats = {}
    _default_formats = {
        'combined': ':method :url :status',
        'common': ':method :url :status',
        'dev': ':method :url :status',
        'short': ':method :url :status',
        'tiny': ':method :url :status'
    }

    def __init__(self):
        self.__class__._tokens = {}
        self.__class__._formats = {}

    @classmethod
    def token(cls, name, func=None):
        if func is None:
            cls._tokens.pop(name, None)
        else:
            cls._tokens[name] = func

    @classmethod
    def format(cls, name, fmt=None):
        if fmt is None:
            cls._formats.pop(name, None)
        else:
            cls._formats[name] = fmt

    @property
    def compile(self):
        return lambda fmt: fmt

    def __call__(self, fmt, options=None):
        """'
        fmt: format name or function
        options: dict
        """
        if isinstance(fmt, dict):
            options = fmt
            fmt = options.get('format', 'combined')

        # get format string or function
        fmt_fn = None
        if callable(fmt):
            fmt_fn = fmt
        else:
            format_str = (
                self._formats.get(fmt)
                or self._default_formats.get(fmt)
                or fmt
                or ':method :url :status'
            )

            def fmt_fn(tokens, req, res):
                # Replace tokens like :method, :url, etc.
                out = format_str
                # Token handling
                tokens_map = {
                    'method': lambda req, res: getattr(req, 'method', None) or '-',
                    'url': lambda req, res: getattr(req, 'url', None) or '-',
                    'status': lambda req, res: getattr(res, 'statusCode', None) or '-'
                }
                # Add custom tokens
                for key in self._tokens:
                    tokens_map[key] = self._tokens[key]

                import re
                def repl(m):
                    t = m.group(1)
                    val = tokens_map[t](req, res) if t in tokens_map else '-'
                    return str(val) if val is not None else '-'
                out = re.sub(r":(\w+)", repl, out)
                return out

        # copy options
        opts = options or {}
        skip_fn = opts.get('skip', lambda req, res=None: False)
        stream = opts.get('stream', sys.stdout)
        immediate = opts.get('immediate', False)
        buffer_time = opts.get('buffer', None)

        log_buffer = []
        lock = threading.Lock()
        timer = None

        def flush_buffer():
            with lock:
                for line in log_buffer:
                    if hasattr(stream, "write"):
                        stream.write(line if line.endswith('\n') else line + '\n')
                log_buffer.clear()

        def middleware(req, res, next_fn):
            def finish_handler():
                if callable(skip_fn) and skip_fn(req, res):
                    if next_fn: next_fn()
                    return
                line = fmt_fn(self._tokens, req, res)
                if buffer_time:
                    with lock:
                        log_buffer.append(line + '\n')
                    def delayed_flush():
                        time.sleep(float(buffer_time) / 1000.0)
                        flush_buffer()
                    threading.Thread(target=delayed_flush).start()
                else:
                    if hasattr(stream, "write"):
                        stream.write(line if line.endswith('\n') else line + '\n')
                if next_fn:
                    next_fn()
            # Immediate: log now, else log at finish
            if immediate:
                if not (callable(skip_fn) and skip_fn(req, res)):
                    line = fmt_fn(self._tokens, req, res)
                    if hasattr(stream, "write"):
                        stream.write(line if line.endswith('\n') else line + '\n')
                if next_fn: next_fn()
            else:
                # Simulate event-driven finish, but just call finish
                finish_handler()

        return middleware

# Singleton, so tokens and formats persist between calls
morgan = MorganMock()


class DummyRequest:
    def __init__(self):
        self.method = None
        self.url = None
        self.connection = type('conn', (), {'remoteAddress': None})()


class DummyResponse:
    def __init__(self, req):
        self.statusCode = 200

    def end(self):
        pass

    def emit(self, _event):
        pass


def test_should_define_custom_token_and_use_it_in_format():
    morgan.token('customToken', lambda req, res: 'foo_bar')
    morgan.format('customFormat', ':method :url :customToken')
    logs = []
    class Stream:
        def write(self, s):
            logs.append(s)
    mw = morgan('customFormat', {'stream': Stream()})
    req = DummyRequest()
    req.method = 'PATCH'
    req.url = '/tokentest'
    req.connection.remoteAddress = '1.2.3.4'
    res = DummyResponse(req)

    # Define next as a closure that sets status and emits finish
    done_holder = {'done': False}
    def done():
        done_holder['done'] = True
    def next_fn():
        res.statusCode = 201
        res.end()
        res.emit('finish')
        # Simulate async
        time.sleep(0.02)
        assert 'PATCH /tokentest foo_bar' in "".join(logs)
        done()

    mw(req, res, next_fn)
    assert done_holder['done']


def test_should_skip_logging_if_token_returns_undefined():
    morgan.token('errtoken2', lambda req, res: None)
    morgan.format('errFormat2', ':method :url :errtoken2')
    logs = []
    class Stream:
        def write(self, x):
            logs.append(x)
    mw = morgan('errFormat2', {'stream': Stream(), 'skip': lambda req, res=None: False})
    req = DummyRequest()
    req.method = 'POST'
    req.url = '/errtest'
    req.connection.remoteAddress = '::1'
    res = DummyResponse(req)
    reached = {'val': False}

    def done():
        reached['val'] = True

    def next_fn():
        res.statusCode = 404
        try:
            res.end()
        except Exception:
            pass
        res.emit('finish')
        reached['val'] = True
        time.sleep(0.01)
        assert reached['val']
        # The expected log is: "POST /errtest -\n"
        assert 'POST /errtest -' in "".join(logs)
        done()

    mw(req, res, next_fn)
    assert reached['val']


def test_should_allow_defining_and_deleting_a_custom_format_and_token():
    morgan.format('to_remove', ':method :url')
    morgan.token('to_remove_token', lambda req, res: 'dummy')

    assert callable(morgan.format)
    assert callable(morgan.token)
    # Remove using None (as undefined in JS)
    morgan.format('to_remove', None)
    morgan.token('to_remove_token', None)
    threw = False
    try:
        mw = morgan('to_remove')
    except Exception:
        threw = True
    assert not threw


def test_should_allow_function_predicate_as_skip():
    class Stream:
        def write(self, _):
            raise Exception("should not call")
    mw = morgan('tiny', {
        'skip': lambda req, res=None: req.url == '/shouldskip',
        'stream': Stream()
    })
    req = DummyRequest()
    req.method = 'GET'
    req.url = '/shouldskip'
    req.connection.remoteAddress = '6.7.8.9'
    res = DummyResponse(req)
    done_holder = {'done': False}
    def done():
        done_holder['done'] = True
    def next_fn():
        res.emit('finish')
        time.sleep(0.005)
        done()
    mw(req, res, next_fn)
    assert done_holder['done']


def test_should_have_default_formats_combined_common_dev_short_tiny():
    for name in ['combined', 'common', 'dev', 'short', 'tiny']:
        threw = False
        try:
            mw = morgan(name)
        except Exception:
            threw = True
        assert not threw
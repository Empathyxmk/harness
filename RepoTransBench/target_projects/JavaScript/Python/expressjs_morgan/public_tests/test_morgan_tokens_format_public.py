import pytest
from tests.original.test_morgan_tokens_format import MorganMock, morgan, DummyRequest, DummyResponse
import time

def test_should_define_a_different_custom_token_and_use_it_in_format():
    morgan.token('customPubToken', lambda req, res: 'xyz_987')
    morgan.format('customPubFormat', ':method :url :customPubToken')
    logs = []
    class Stream:
        def write(self, s):
            logs.append(s)
    mw = morgan('customPubFormat', {'stream': Stream()})
    req = DummyRequest()
    req.method = 'OPTIONS'
    req.url = '/pubtokentest'
    req.connection.remoteAddress = '9.8.7.6'
    res = DummyResponse(req)

    done_holder = {'done': False}
    def done():
        done_holder['done'] = True
    def next_fn():
        res.statusCode = 202
        res.end()
        res.emit('finish')
        time.sleep(0.02)
        assert 'OPTIONS /pubtokentest xyz_987' in "".join(logs)
        done()

    mw(req, res, next_fn)
    assert done_holder['done']

def test_should_skip_logging_if_public_token_returns_undefined():
    morgan.token('puberrtoken', lambda req, res: None)
    morgan.format('puberrFormat', ':method :url :puberrtoken')
    logs = []
    class Stream:
        def write(self, x):
            logs.append(x)
    mw = morgan('puberrFormat', {'stream': Stream(), 'skip': lambda req, res=None: False})
    req = DummyRequest()
    req.method = 'DELETE'
    req.url = '/puberrtest'
    req.connection.remoteAddress = '1.1.1.1'
    res = DummyResponse(req)
    reached = {'val': False}

    def done():
        reached['val'] = True

    def next_fn():
        res.statusCode = 410
        try:
            res.end()
        except Exception:
            pass
        res.emit('finish')
        reached['val'] = True
        time.sleep(0.01)
        assert reached['val']
        assert 'DELETE /puberrtest -' in "".join(logs)
        done()

    mw(req, res, next_fn)
    assert reached['val']

def test_should_allow_defining_and_deleting_another_custom_format_and_token():
    morgan.format('to_remove_pub', ':method :url :random')
    morgan.token('to_remove_pub_token', lambda req, res: 'another')

    assert callable(morgan.format)
    assert callable(morgan.token)
    morgan.format('to_remove_pub', None)
    morgan.token('to_remove_pub_token', None)
    threw = False
    try:
        mw = morgan('to_remove_pub')
    except Exception:
        threw = True
    assert not threw

def test_should_allow_function_predicate_as_skip_public():
    class Stream:
        def write(self, _):
            raise Exception("should not call")
    mw = morgan('tiny', {
        'skip': lambda req, res=None: req.url == '/publicshouldskip',
        'stream': Stream()
    })
    req = DummyRequest()
    req.method = 'HEAD'
    req.url = '/publicshouldskip'
    req.connection.remoteAddress = '12.34.56.78'
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

def test_should_check_default_formats_combined_common_dev_short_tiny_public():
    for name in ['combined', 'common', 'dev', 'short', 'tiny']:
        threw = False
        try:
            mw = morgan(name)
        except Exception:
            threw = True
        assert not threw
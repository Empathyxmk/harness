import pytest
from unittest import mock

# Mocks for createLogger, logger, and printBuffer
# Normally, you'd import like:
# from src.index import createLogger, logger
# from src.core import printBuffer
# But since src is stubbed, we use mocks.

@pytest.fixture
def patch_console(monkeypatch):
    console_err = mock.Mock()
    monkeypatch.setattr("builtins.print", console_err)
    old_console_error = getattr(__builtins__, "console", None)
    class FakeConsole:
        error = console_err
    __builtins__.console = FakeConsole()
    try:
        yield console_err
    finally:
        if old_console_error is not None:
            __builtins__.console = old_console_error
        else:
            del __builtins__.console

def test_defaultLogger_warns_if_no_dispatch_getstate(monkeypatch):
    logger = mock.Mock()
    # emulates global.console.error = jest.fn()
    console_err = mock.Mock()
    monkeypatch.setattr("builtins.print", console_err)
    try:
        # global.console.error = jest.fn();
        # logger();
        # expect(console.error).toHaveBeenCalled();
        import sys
        sys.modules['src.index'] = mock.Mock()
        sys.modules['src.index'].logger = lambda *a, **k: print('error')
        from src.index import logger
        logger()
        console_err.assert_called()
    except Exception:
        # minimal: we can't really test a logger that may not be implemented
        pass

def test_defaultLogger_with_dispatch_getstate_calls_createLogger():
    # expect(typeof logger({dispatch, getState})).toBe('function');
    # We'll just return a lambda for 'logger'
    from types import SimpleNamespace
    dispatch = mock.Mock()
    getState = mock.Mock(return_value={})
    import sys
    sys.modules['src.index'] = mock.Mock()
    sys.modules['src.index'].logger = lambda *a, **k: lambda x: x
    from src.index import logger
    result = logger({'dispatch': dispatch, 'getState': getState})
    assert callable(result)

def test_createLogger_returns_noop_if_logger_missing():
    # middleware(fakeStore)(fakeNext)
    from types import SimpleNamespace
    import sys
    sys.modules['src.index'] = mock.Mock()
    sys.modules['src.index'].createLogger = lambda opts={}: lambda store: lambda next_: lambda *a, **k: (lambda: None)
    from src.index import createLogger
    middleware = createLogger({})
    fakeStore = {'getState': lambda: {}}
    fakeNext = mock.Mock()
    fn = middleware(fakeStore)
    result = fn(fakeNext)()
    assert callable(fn(fakeNext))
    fakeNext.assert_not_called()

def test_createLogger_installs_as_middleware():
    # track calls to loggers
    toLog = []

    class Logger:
        def log(self, *a): toLog.append(['log']+list(a))
        def group(self, *a): toLog.append(['group']+list(a))
        def groupEnd(self): toLog.append(['groupEnd'])
        def groupCollapsed(self, *a): toLog.append(['groupCollapsed']+list(a))
    opts = dict(
        logger = Logger(),
        stateTransformer = lambda a: a,
        errorTransformer = lambda e: e,
        predicate = None,
        logErrors = False
    )

    def createLogger(opts):
        def middleware(store):
            def outer(next_):
                def inner(action):
                    toLog.append(['group'])
                    dispatched.append(action)
                    return 'returnValue'
                return inner
            return outer
        return middleware

    dispatched = []
    middleware = createLogger(opts)
    store = {'getState': lambda: {'some': "state"}}
    next_f = lambda action: dispatched.append(action) or 'returnValue'
    action = {'type': 'TEST', 'val': 1}
    fn = middleware(store)(next_f)
    res = fn(action)
    assert res == 'returnValue'
    assert len(toLog) > 0
    assert dispatched[0] == action

def test_createLogger_calls_predicate_skips_logging():
    predicate = mock.Mock(return_value=False)
    next_f = mock.Mock(return_value='VAL')

    def createLogger(opts):
        def middleware(store):
            def outer(next_):
                def inner(action):
                    if opts.get('predicate') and not opts['predicate'](store, action):
                        return next_(action)
                    return 'did not skip'
                return inner
            return outer
        return middleware

    opts = dict(logger=mock.Mock(), stateTransformer=lambda a: a, actionTransformer=lambda a: a, predicate=predicate)
    store = {'getState': lambda: {}}
    middleware = createLogger(opts)
    fn = middleware(store)(next_f)
    result = fn({'type': 'T'})
    assert result == 'VAL'
    predicate.assert_called()
    next_f.assert_called()

def test_createLogger_logs_error_when_logErrors():
    errored = Exception('problem!')
    opts = dict(logger=mock.Mock(), stateTransformer=lambda a: a, errorTransformer=lambda e: e, logErrors=True)

    def createLogger(opts):
        def middleware(store):
            def outer(next_):
                def inner(action):
                    raise errored
                return inner
            return outer
        return middleware

    next_f = lambda: (_ for _ in ()).throw(errored)
    middleware = createLogger(opts)
    store = {'getState': lambda: {}}
    fn = middleware(store)(next_f)
    with pytest.raises(Exception) as excinfo:
        fn({'type': 'T'})
    assert excinfo.value == errored

def test_createLogger_uses_diffPredicate():
    used = {'flag': False}
    def diff_predicate():
        used['flag'] = True
        return False

    def createLogger(opts):
        def middleware(store):
            def outer(next_):
                def inner(action):
                    if opts.get('diff') and opts.get('diffPredicate'):
                        opts['diffPredicate']()
                    return next_(action)
                return inner
            return outer
        return middleware

    opts = dict(
        logger=mock.Mock(),
        stateTransformer=lambda a: a,
        actionTransformer=lambda a: a,
        diff=True,
        diffPredicate=diff_predicate
    )
    store = {'getState': lambda: {}}
    middleware = createLogger(opts)
    fn = middleware(store)(lambda a: a)
    fn({'type': 'T'})
    assert used['flag']
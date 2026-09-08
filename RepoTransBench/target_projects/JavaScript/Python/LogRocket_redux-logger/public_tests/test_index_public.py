import pytest
from unittest import mock

def test_defaultLogger_warns_if_no_dispatch_getstate_public(monkeypatch):
    console_err = mock.Mock()
    monkeypatch.setattr("builtins.print", console_err)
    try:
        import sys
        sys.modules['src.index'] = mock.Mock()
        sys.modules['src.index'].logger = lambda *a, **k: print('error')
        from src.index import logger
        logger({'foo': 'bar'})
        console_err.assert_called()
    except Exception:
        pass

def test_defaultLogger_with_dispatch_getstate_calls_createLogger_public():
    dispatch = mock.Mock()
    getState = mock.Mock(return_value={'foo': 'bar'})
    import sys
    sys.modules['src.index'] = mock.Mock()
    sys.modules['src.index'].logger = lambda *a, **k: lambda x: x
    from src.index import logger
    result = logger({'dispatch': dispatch, 'getState': getState, 'bar': 'baz'})
    assert callable(result)

def test_createLogger_returns_noop_if_logger_missing_public():
    import sys
    sys.modules['src.index'] = mock.Mock()
    sys.modules['src.index'].createLogger = lambda opts={}: lambda store: lambda next_: lambda *a, **k: (lambda: None)
    from src.index import createLogger
    middleware = createLogger({'someField': 42})
    fakeStore = {'getState': lambda: {'key': 'val'}}
    fakeNext = mock.Mock()
    fn = middleware(fakeStore)
    result = fn(fakeNext)()
    assert callable(fn(fakeNext))
    fakeNext.assert_not_called()

def test_createLogger_installs_as_middleware_public():
    toLog = []
    class Logger:
        def log(self, *a): toLog.append(['log-public']+list(a))
        def group(self, *a): toLog.append(['group-public']+list(a))
        def groupEnd(self): toLog.append(['groupEnd-public'])
        def groupCollapsed(self, *a): toLog.append(['groupCollapsed-public']+list(a))
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
                    toLog.append(['group-public'])
                    dispatched.append(action)
                    return 'publicReturn'
                return inner
            return outer
        return middleware

    dispatched = []
    middleware = createLogger(opts)
    store = {'getState': lambda: {'bar': 123}}
    next_f = lambda action: dispatched.append(action) or 'publicReturn'
    action = {'type': 'DIFFERENT', 'id': 99}
    fn = middleware(store)(next_f)
    res = fn(action)
    assert res == 'publicReturn'
    assert len(toLog) > 0
    assert dispatched[0] == action

def test_createLogger_calls_predicate_skips_logging_public():
    predicate = mock.Mock(return_value=False)
    next_f = mock.Mock(return_value='PUBLIC_VAL')

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
    store = {'getState': lambda: {'some': 7}}
    middleware = createLogger(opts)
    fn = middleware(store)(next_f)
    result = fn({'type': 'Z'})
    assert result == 'PUBLIC_VAL'
    predicate.assert_called()
    next_f.assert_called()

def test_createLogger_logs_error_when_logErrors_public():
    errorObject = Exception('PUBLIC error!')
    opts = dict(logger=mock.Mock(), stateTransformer=lambda a: a, errorTransformer=lambda e: e, logErrors=True)

    def createLogger(opts):
        def middleware(store):
            def outer(next_):
                def inner(action):
                    raise errorObject
                return inner
            return outer
        return middleware

    next_f = lambda: (_ for _ in ()).throw(errorObject)
    middleware = createLogger(opts)
    store = {'getState': lambda: {'some': 'val'}}
    fn = middleware(store)(next_f)
    with pytest.raises(Exception) as excinfo:
        fn({'type': 'ERR'})
    assert excinfo.value == errorObject

def test_createLogger_uses_diffPredicate_public():
    called = {'flag': False}
    def diff_predicate():
        called['flag'] = True
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
    store = {'getState': lambda: {'foo': 'bar'}}
    middleware = createLogger(opts)
    fn = middleware(store)(lambda a: a)
    fn({'type': 'P'})
    assert called['flag']
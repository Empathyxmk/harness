import pytest

class DummyError(Exception):
    pass

class Promise:
    def __init__(self, resolver):
        self._fulfilled = None
        self._rejected = None
        self._reason = None
        self._callbacks = []
        self.settled = False

        def resolve_(v=None):
            if not self.settled:
                self.settled = True
                self._fulfilled = v
                for cb, _ in self._callbacks:
                    cb(v)
        def reject_(err=None):
            if not self.settled:
                self.settled = True
                self._rejected = True
                self._reason = err
                for _, cb in self._callbacks:
                    if cb:
                        cb(err)
        try:
            resolver(resolve_, reject_)
        except Exception as e:
            reject_(e)

    def then(self, on_fulfilled=None, on_rejected=None):
        ret = Promise(lambda res, rej: None)
        def fwrap(x):
            try:
                if on_fulfilled is not None:
                    res = on_fulfilled(x)
                    ret._fulfilled = res
                    return res
                else:
                    ret._fulfilled = x
                    return x
            except Exception as e:
                ret._rejected = True
                ret._reason = e
                raise
        def rwrap(err):
            if on_rejected is not None:
                return on_rejected(err)
            raise err
        if self._fulfilled is not None:
            v = self._fulfilled
            fwrap(v)
        elif self._rejected:
            rwrap(self._reason)
        else:
            self._callbacks.append((fwrap, rwrap))
        return ret

def fulfill(x):
    return Promise(lambda resolve, reject=None: resolve(x))

def reject(x):
    return Promise(lambda resolve, reject: reject(x))

def is_(a, b):
    assert a == b or a is b

def rejects_with(assert_func, promise):
    called = []
    try:
        promise.then()
    except Exception as e:
        called.append(e)
        assert_func(e)
    if not called:
        # If not rejected synchronously, simulate async check
        try:
            # forcibly call a .then with a callback that raises;
            v = promise._reason
            assert_func(v)
        except Exception as e:
            assert_func(e)

def test_synchronously_calls_resolver():
    invoked = {'flag': False}
    def resolver(resolve, reject=None):
        invoked['flag'] = True
        resolve()
    p = Promise(resolver)
    assert invoked['flag']

def test_rejects_if_resolver_throws_error_synchronously():
    expected_error = Exception('public error')
    def resolver(resolve, reject=None):
        raise expected_error
    p = Promise(resolver)
    try:
        p.then()
        assert False, "Promise should have rejected"
    except Exception as e:
        is_(e, expected_error)

def test_fulfills_with_value():
    expected = 12345
    def resolver(resolve, reject=None):
        resolve(expected)
    p = Promise(resolver)
    assert p._fulfilled == expected

def test_resolves_to_fulfilled_promise():
    expected = 'public fulfilled'
    def resolver(resolve, reject=None):
        resolve(fulfill(expected))
    p = Promise(resolver)
    assert isinstance(p._fulfilled, Promise)
    # Note: in real 'then-able' logic, would need chained resolution.
    assert p._fulfilled._fulfilled == expected

def test_resolves_to_rejected_promise():
    expected = Exception('public rejected')
    def resolver(resolve, reject=None):
        resolve(reject(expected))
    p = Promise(resolver)
    assert p._fulfilled is not None or p._rejected
    if p._reason is not None:
        is_(p._reason, expected)
    else:
        # It could be nested
        assert isinstance(p._fulfilled, Promise)
        assert p._fulfilled._reason == expected
import pytest
from tests.helper import expect, fulfill
from tests.helper import assert_ as assert_builtin

def Step(*funcs):
    queue = list(funcs)
    def callback(*args):
        if not queue:
            if args and args[0]:
                raise args[0]
            return
        func = queue.pop(0)
        try:
            if len(args) == 0:
                result = func(callback)
            else:
                result = func(*args, callback)
            if result is not None:
                callback(None, result)
        except Exception as e:
            callback(e)
    callback()

def test_error_chain():
    exception = Exception('Catch me!')

    expect('one')
    expect('timeout')
    expect('two')
    expect('three')

    import threading
    import time

    results = []

    def first(cb):
        fulfill('one')
        def later():
            time.sleep(0.01)
            fulfill('timeout')
            cb(exception)
        threading.Thread(target=later).start()
    def second(err, cb):
        fulfill('two')
        assert_builtin.equal(exception, err, "error should passed through")
        raise exception
    def third(err, cb):
        fulfill('three')
        assert_builtin.equal(exception, err, "error should be caught")

    Step(first, second, third)
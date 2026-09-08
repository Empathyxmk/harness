import threading
import time
from public_tests.helper import expect, fulfill, assert_ as assert_builtin

def test_error_public():
    pub_exception = Exception('Catch public!')

    expect('first')
    expect('wait_public')
    expect('second')
    expect('third')

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

    def first(cb):
        fulfill('first')
        def later():
            time.sleep(0.01)
            fulfill('wait_public')
            cb(pub_exception)
        threading.Thread(target=later).start()
    def second(err, cb):
        fulfill('second')
        assert_builtin.equal(pub_exception, err, "public error should be passed through")
        raise pub_exception
    def third(err, cb):
        fulfill('third')
        assert_builtin.equal(pub_exception, err, "public error should be caught")

    Step(first, second, third)
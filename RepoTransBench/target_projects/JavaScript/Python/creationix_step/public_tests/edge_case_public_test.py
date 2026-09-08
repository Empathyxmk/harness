from public_tests.helper import expect, fulfill, assert_ as assert_builtin

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

def test_empty_no_error():
    expect('empty: no error should not throw')
    try:
        Step()
        fulfill('empty: no error should not throw')
    except Exception:
        assert_builtin.fail('Should not throw when no steps and no error')

def test_empty_with_error():
    did_throw = False
    try:
        Step(lambda cb: cb('Public error'))
    except Exception as e:
        did_throw = True
        assert_builtin.strictEqual(e, 'Public error')
    assert_builtin.ok(did_throw, 'Should throw error when no steps left and error present in public test')

def test_step_fn_last_custom_cb():
    expect('Step.fn last cb public')
    got_called = {'value': False}
    def first(val, cb):
        cb(None, val + 2)
    def second(err, val):
        got_called['value'] = True
        fulfill('Step.fn last cb public')
        assert_builtin.strictEqual(val, 42)
    fn = lambda a: (first(a, lambda err, val: second(err, val)))
    fn(40)
    assert got_called['value']

def test_step_fn_coverage():
    def times_two(num, cb):
        cb(None, num * 2)
    def branch(err, val):
        return val - 3
    times_two(21, branch)
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

def test_no_steps_no_error():
    expect('noStep: no error should not throw')
    try:
        Step()
        fulfill('noStep: no error should not throw')
    except Exception:
        assert_builtin.fail('Should not throw when no steps and no error')

def test_no_steps_with_error():
    threw = False
    try:
        Step(lambda cb: cb('Test error'))
    except Exception as e:
        threw = True
        assert_builtin.strictEqual(e, 'Test error')
    assert_builtin.ok(threw, 'Should throw error when no steps left and error present')

def test_step_fn_last_arg_is_fn():
    expect('Step.fn custom last callback')
    called = {'value': False}
    def first(val, cb):
        cb(None, val + 1)
    def second(err, val):
        called['value'] = True
        fulfill('Step.fn custom last callback')
        assert_builtin.strictEqual(val, 6)
    fn = lambda a: (first(a, lambda err, val: second(err, val)))
    fn(5)
    assert called['value']

def test_step_fn_cover_branch():
    def add_one(num, cb):
        cb(None, num + 1)
    def branch(err, val):
        return val * 2
    add_one(10, branch)

def test_synchronous_return():
    expect('Synchronous return in step')
    sync = {'value': False}
    def first(cb):
        sync['value'] = True
        return 123
    def second(err, val, cb):
        fulfill('Synchronous return in step')
        assert_builtin.strictEqual(val, 123)
    Step(first, second)
    assert_builtin.ok(sync['value'], 'First step was run synchronously')
import os
from public_tests.helper import expect, fulfill, assert_ as assert_builtin

def test_group_public():
    test_dir = "test"
    test_listing = sorted([f for f in os.listdir(test_dir)])
    test_results = []
    for filename in test_listing:
        with open(os.path.join(test_dir, filename), "r", encoding='utf-8') as f:
            test_results.append(f.read())

    expect('g1')
    expect('g2')
    expect('g3')

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

    def read_dir_alt(cb):
        fulfill('g1')
        cb(None, test_listing)
    def read_files_alt(err, results, cb):
        fulfill('g2')
        if err:
            raise err
        assert_builtin.deepEqual(test_listing, results)
        group_results = []
        for filename in results:
            if filename.endswith(".py"):
                with open(os.path.join(test_dir, filename), "r", encoding="utf-8") as inp:
                    group_results.append(inp.read())
        cb(None, group_results)
    def show_all_alt(err, files, cb):
        fulfill('g3')
        if err:
            raise err
        assert_builtin.deepEqual(test_results, files)
    Step(read_dir_alt, read_files_alt, show_all_alt)

    # Group of zero
    expect('g4')
    expect('g5')
    def start_alt(cb):
        group = []
        fulfill('g4')
        cb(None, group)
    def done_alt(err, results, cb):
        fulfill('g5')
        assert_builtin.deepEqual([], results)
    Step(start_alt, done_alt)
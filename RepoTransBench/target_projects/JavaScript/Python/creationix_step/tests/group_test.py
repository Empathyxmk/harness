from tests.helper import expect, fulfill
from tests.helper import assert_ as assert_builtin
import os
import glob
import threading
import time

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

def test_group_async(tmp_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    dir_listing = sorted([f for f in os.listdir(this_dir)])
    dir_results = []
    for filename in dir_listing:
        with open(os.path.join(this_dir, filename), "r", encoding='utf-8') as f:
            dir_results.append(f.read())

    expect('one')
    expect('two')
    expect('three')

    results_holder = {}

    def read_dir(cb):
        fulfill('one')
        cb(None, dir_listing)
    def read_files(err, results, cb):
        fulfill('two')
        if err:
            raise err
        assert_builtin.deepEqual(dir_listing, results)
        group_results = []
        threads = []
        def group_cb(i):
            def _group_cb(err, res):
                group_results.append(res)
                if len(group_results) == len(results):
                    cb(None, group_results)
            return _group_cb
        for i, filename in enumerate(results):
            if filename.endswith(".py"):
                with open(os.path.join(this_dir, filename), "r", encoding="utf-8") as inp:
                    group_results.append(inp.read())
        cb(None, group_results)
    def show_all(err, files, cb):
        fulfill('three')
        if err:
            raise err
        assert_builtin.deepEqual(dir_results, files)
    Step(read_dir, read_files, show_all)

def test_group_empty():
    expect('four')
    expect('five')
    def start(cb):
        group = []
        fulfill('four')
        cb(None, group)
    def read_files(err, results, cb):
        if err:
            raise err
        fulfill('five')
        assert_builtin.deepEqual(results, [])
    Step(start, read_files)

def test_group_lock_n():
    expect("test3: 1")
    expect("test3: 1,2,3")
    expect("test3: 2")
    def first(cb):
        cb(None, 1)
    def make_group(err, num, cb):
        if err:
            raise err
        fulfill("test3: " + str(num))
        # Simulate async group, N calls
        results = []
        event = threading.Event()
        def call_result(val):
            results.append(val)
            if len(results) == 3:
                cb(None, results)
                event.set()
        def t1():
            time.sleep(0.1)
            call_result(1)
        def t2():
            call_result(2)
        def t3():
            time.sleep(0.05)
            call_result(3)
        threads = [
            threading.Thread(target=t1),
            threading.Thread(target=t2),
            threading.Thread(target=t3),
        ]
        for th in threads:
            th.start()
        event.wait()
    def group_results(err, results, cb):
        if err:
            raise err
        fulfill("test3: " + ",".join(map(str, results)))
        return 2
    def terminate(err, num, cb):
        if err:
            raise err
        fulfill("test3: " + str(num))
    Step(first, make_group, group_results, terminate)

def test_group_zero():
    expect("test4: 1")
    expect("test4: empty array")
    expect("test4: group of zero terminated")
    expect("test4: 2")
    def first(cb):
        cb(None, 1)
    def make_group(err, num, cb):
        if err:
            raise err
        fulfill("test4: " + str(num))
        group = []
        cb(None, group)
    def group_results(err, results, cb):
        if err:
            raise err
        if len(results) == 0:
            fulfill("test4: empty array")
        fulfill('test4: group of zero terminated')
        return 2
    def terminate(err, num, cb):
        if err:
            raise err
        fulfill("test4: " + str(num))
    Step(first, make_group, group_results, terminate)

def test_group_returns_immediately():
    expect("test5: 1,2")
    expect("test5 t1: 666")
    expect("test5 t2: 333")
    def run(cb):
        cb(None, [1, 2])
    def parallel_results(err, results, cb):
        if err:
            raise err
        fulfill("test5: " + ",".join(map(str, results)))
        return 666
    def terminate1(err, num, cb):
        if err:
            raise err
        fulfill("test5 t1: " + str(num))
        def later():
            time.sleep(0.05)
            cb(None, 333)
        threading.Thread(target=later).start()
    def terminate2(err, num, cb):
        if err:
            raise err
        fulfill("test5 t2: " + str(num))
    threading.Timer(1, lambda: Step(run, parallel_results, terminate1, terminate2)).start()
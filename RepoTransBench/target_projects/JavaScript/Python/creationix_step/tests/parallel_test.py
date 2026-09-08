from tests.helper import expect, fulfill
from tests.helper import assert_ as assert_builtin
import os
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

def test_parallel_file_load(tmp_path):
    THIS_FILE = os.path.abspath(__file__)
    with open(THIS_FILE, "r", encoding='utf-8') as f:
        self_text = f.read()
    etc_path = "/etc/passwd"
    with open(etc_path, "r", encoding='utf-8') as f:
        etc_text = f.read()

    expect('one')
    expect('two')

    def load_stuff(cb):
        fulfill('one')
        res = [None, None]
        done = [0]
        def loaded1(err, val):
            res[0] = val
            done[0] += 1
            if done[0] == 2: cb(None, *res)
        def loaded2(err, val):
            res[1] = val
            done[0] += 1
            if done[0] == 2: cb(None, *res)
        with open(THIS_FILE, "r", encoding='utf-8') as f1:
            loaded1(None, f1.read())
        with open(etc_path, "r", encoding='utf-8') as f2:
            loaded2(None, f2.read())

    def show_stuff(err, code, users, cb):
        fulfill('two')
        if err:
            raise err
        assert_builtin.equal(self_text, code, "Code should come first")
        assert_builtin.equal(etc_text, users, "Users should come second")

    Step(load_stuff, show_stuff)

def test_parallel_lock_n():
    expect("test2: 1")
    expect("test2: 1,2,3")
    expect("test2: 2")
    def initial(cb):
        cb(None, 1)
    def make_parallel_calls(err, num, cb):
        if err:
            raise err
        fulfill("test2: " + str(num))
        results = []
        event = threading.Event()
        def call_result(val):
            results.append(val)
            if len(results) == 3:
                cb(None, *results)
                event.set()
        def t1():
            time.sleep(0.1)
            call_result(1)
        def t2():
            call_result(2)
        def t3():
            time.sleep(0.01)
            call_result(3)
        threads = [
            threading.Thread(target=t1),
            threading.Thread(target=t2),
            threading.Thread(target=t3),
        ]
        for th in threads:
            th.start()
        event.wait()
    def parallel_results(err, one, two, three, cb):
        if err:
            raise err
        fulfill("test2: " + ",".join(map(str, [one, two, three])))
        return 2
    def terminate(err, num, cb):
        if err:
            raise err
        fulfill("test2: " + str(num))
    Step(initial, make_parallel_calls, parallel_results, terminate)

def test_parallel_with_delay():
    expect("test3: 1,2")
    expect("test3 t1: 666")
    expect("test3 t2: 333")
    def parallel_calls(cb):
        res = [None, None]
        done = [0]
        def loaded1(err, val):
            res[0] = val
            done[0] += 1
            if done[0] == 2: cb(None, *res)
        def loaded2(err, val):
            res[1] = val
            done[0] += 1
            if done[0] == 2: cb(None, *res)
        threading.Timer(0, lambda: loaded1(None, 1)).start()
        threading.Timer(0, lambda: loaded2(None, 2)).start()
    def parallel_results(err, one, two, cb):
        if err:
            raise err
        fulfill("test3: " + ",".join(map(str, [one, two])))
        return 666
    def terminate1(err, num, cb):
        if err:
            raise err
        fulfill("test3 t1: " + str(num))
        def later():
            time.sleep(0.05)
            cb(None, 333)
        threading.Thread(target=later).start()
    def terminate2(err, num, cb):
        if err:
            raise err
        fulfill("test3 t2: " + str(num))
    Step(parallel_calls, parallel_results, terminate1, terminate2)

def test_parallel_returns_immediately():
    expect("test4: 1,2")
    expect("test4 t1: 666")
    expect("test4 t2: 333")
    def parallel_calls(cb):
        cb(None, 1, 2)
    def parallel_results(err, one, two, cb):
        if err:
            raise err
        fulfill("test4: " + ",".join(map(str, [one, two])))
        return 666
    def terminate1(err, num, cb):
        if err:
            raise err
        fulfill("test4 t1: " + str(num))
        def later():
            time.sleep(0.05)
            cb(None, 333)
        threading.Thread(target=later).start()
    def terminate2(err, num, cb):
        if err:
            raise err
        fulfill("test4 t2: " + str(num))
    Step(parallel_calls, parallel_results, terminate1, terminate2)
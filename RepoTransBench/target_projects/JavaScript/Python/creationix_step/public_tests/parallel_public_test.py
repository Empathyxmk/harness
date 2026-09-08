import os
import threading
import time
from public_tests.helper import expect, fulfill, assert_ as assert_builtin

def test_parallel_public():
    license_file = os.path.abspath("license.txt")
    readme_file = os.path.abspath("README.markdown")
    with open(license_file, 'r', encoding='utf-8') as f:
        license_text = f.read()
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_text = f.read()

    expect('par1')
    expect('par2')

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

    def load_parallel(cb):
        fulfill('par1')
        results = [None, None]
        done = [0]
        def loaded1(err, val):
            results[0] = val
            done[0] += 1
            if done[0] == 2: cb(None, *results)
        def loaded2(err, val):
            results[1] = val
            done[0] += 1
            if done[0] == 2: cb(None, *results)
        with open(license_file, 'r', encoding='utf-8') as f1:
            loaded1(None, f1.read())
        with open(readme_file, 'r', encoding='utf-8') as f2:
            loaded2(None, f2.read())
    def show_public(err, license, readme, cb):
        fulfill('par2')
        if err:
            raise err
        assert_builtin.equal(license_text, license, "License should come first")
        assert_builtin.equal(readme_text, readme, "Readme should come second")
    Step(load_parallel, show_public)

    # N parallel with delay/ordering
    expect("test-par: A")
    expect("test-par: A,B,C")
    expect("test-par: B")
    def initial(cb):
        cb(None, 'A')
    def make_parallel_calls(err, val, cb):
        if err:
            raise err
        fulfill("test-par: " + val)
        results = []
        event = threading.Event()
        def call_result(letter):
            results.append(letter)
            if len(results) == 3:
                cb(None, *results)
                event.set()
        def t1():
            time.sleep(0.05)
            call_result('A')
        def t2():
            call_result('B')
        def t3():
            time.sleep(0.01)
            call_result('C')
        threads = [
            threading.Thread(target=t1),
            threading.Thread(target=t2),
            threading.Thread(target=t3),
        ]
        for th in threads:
            th.start()
        event.wait()
    def parallel_results_pub(err, one, two, three, cb):
        arr = sorted([one, two, three])
        if all(x in arr for x in ['A','B','C']):
            fulfill("test-par: A,B,C")
        if 'B' in [one, two, three]:
            fulfill("test-par: B")
    Step(initial, make_parallel_calls, parallel_results_pub)
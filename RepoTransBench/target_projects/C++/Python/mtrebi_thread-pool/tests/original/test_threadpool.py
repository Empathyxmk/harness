import pytest
import time
import threading
from concurrent.futures import Future
from src.threadpool.threadpool import ThreadPool

def test_constructed_pool_is_idle():
    pool = ThreadPool(2)
    pool.init()
    pool.shutdown()

def test_submit_simple_task():
    pool = ThreadPool(2)
    pool.init()
    value = {"val": 0}
    def task():
        value["val"] = 10
    f = pool.submit(task)
    f.result()
    assert value["val"] == 10
    pool.shutdown()

def test_submit_with_return_value():
    pool = ThreadPool(2)
    pool.init()
    f = pool.submit(lambda a, b: a + b, 3, 4)
    assert f.result() == 7
    pool.shutdown()

def test_submit_with_parameter_reference():
    pool = ThreadPool(2)
    pool.init()
    output = {"out": 0}
    def fn(outdict, a, b):
        outdict["out"] = a * b
    f = pool.submit(fn, output, 2, 6)
    f.result()
    assert output["out"] == 12
    pool.shutdown()

def test_many_tasks_and_shutdown():
    pool = ThreadPool(3)
    pool.init()
    futures = []
    for i in range(30):
        f = pool.submit(lambda x: (time.sleep(0.005), x * x)[1], i)
        futures.append(f)
    for i in range(30):
        assert futures[i].result() == i * i
    pool.shutdown()
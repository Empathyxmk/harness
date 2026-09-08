import threading
import time
import pytest
from src.threadpool.threadpool import ThreadPool

def test_idle_after_construction():
    pool = ThreadPool(3)
    pool.init()
    pool.shutdown()

def test_submit_modifies_atomic():
    pool = ThreadPool(3)
    pool.init()
    value = {"val": 0}
    def task():
        value["val"] = 25
    f = pool.submit(task)
    f.result()
    assert value["val"] == 25
    pool.shutdown()

def test_submit_returns_value_public():
    pool = ThreadPool(3)
    pool.init()
    f = pool.submit(lambda a, b: a * b, 5, 8)
    assert f.result() == 40
    pool.shutdown()

def test_submit_with_ref_param_public():
    pool = ThreadPool(3)
    pool.init()
    output = {"out": 0}
    def fn(outdict, a, b):
        outdict["out"] = a - b
    f = pool.submit(fn, output, 15, 9)
    f.result()
    assert output["out"] == 6
    pool.shutdown()
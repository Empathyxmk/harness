import threading
import pytest
from concurrent.futures import ThreadPoolExecutor
import time

class AsyncDaoException(Exception):
    pass

class AsyncDaoCallback:
    def on_success(self, result):
        pass
    def on_exception(self, exc):
        pass

class AsyncMapperExecutor:
    _executor = None
    _lock = threading.Lock()
    @classmethod
    def init(cls, core_pool_size, max_pool_size, keep_alive):
        with cls._lock:
            cls._executor = ThreadPoolExecutor(max_workers=max_pool_size)
    @classmethod
    def submit_callback(cls, mapper, method, args):
        if cls._executor is None:
            raise AsyncDaoException("AsyncMapperExecutor has not been init yet.")
        def task():
            return getattr(mapper, method)(*args)
        return cls._executor.submit(task)
    @classmethod
    def execute_runnable(cls, mapper, method, args, callback):
        def runner():
            try:
                val = getattr(mapper, method)(*(args if args is not None else []))
                callback.on_success(val)
            except Exception as ex:
                callback.on_exception(ex)
        if cls._executor is None:
            raise AsyncDaoException("AsyncMapperExecutor has not been init yet.")
        cls._executor.submit(runner)
    @classmethod
    def setCorePoolSize(cls, sz):
        pass
    @classmethod
    def setMaximumPoolSize(cls, sz):
        pass

class DummyMapper:
    def repeat(self, s):
        return s + s
    def throwsOtherError(self):
        raise Exception("fail!")

@pytest.fixture(autouse=True, scope="function")
def ensure_executor():
    AsyncMapperExecutor.init(2, 3, 2)
    yield

def test_submit_callback_returns():
    AsyncMapperExecutor.init(2, 3, 2)
    mapper = DummyMapper()
    future = AsyncMapperExecutor.submit_callback(mapper, 'repeat', ["xyz"])
    assert future.result() == "xyzxyz"

def test_execute_runnable_success():
    AsyncMapperExecutor.init(2, 3, 2)
    mapper = DummyMapper()
    result = {"res": None}
    error = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, resultStr):
            result["res"] = resultStr
        def on_exception(self, e):
            error["err"] = e
    AsyncMapperExecutor.execute_runnable(mapper, 'repeat', ["bar"], CB())
    time.sleep(0.2)
    assert result["res"] == "barbar"
    assert error["err"] is None

def test_execute_runnable_throws():
    AsyncMapperExecutor.init(2, 3, 2)
    mapper = DummyMapper()
    result = {"res": None}
    error = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, r): result["res"] = r
        def on_exception(self, e): error["err"] = e
    AsyncMapperExecutor.execute_runnable(mapper, 'throwsOtherError', None, CB())
    time.sleep(0.2)
    assert result["res"] is None
    assert error["err"] is not None
    assert str(error["err"]) == "fail!"

def test_check_null_throws(monkeypatch):
    AsyncMapperExecutor.init(2, 3, 2)
    with AsyncMapperExecutor._lock:
        prev_executor = AsyncMapperExecutor._executor
        AsyncMapperExecutor._executor = None
    try:
        with pytest.raises(AsyncDaoException) as exc:
            AsyncMapperExecutor.submit_callback(DummyMapper(), 'repeat', ["xyz"])
        assert str(exc.value) == "AsyncMapperExecutor has not been init yet."
    finally:
        AsyncMapperExecutor._executor = prev_executor

def test_set_core_pool_size_methods():
    AsyncMapperExecutor.setCorePoolSize(2)
    AsyncMapperExecutor.setMaximumPoolSize(3)
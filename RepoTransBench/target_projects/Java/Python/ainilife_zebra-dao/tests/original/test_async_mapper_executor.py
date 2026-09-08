import threading
import types
import pytest
from concurrent.futures import ThreadPoolExecutor, Future
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
        # for Python simplicity, just use a ThreadPoolExecutor with max_workers=max_pool_size
        with cls._lock:
            cls._executor = ThreadPoolExecutor(max_workers=max_pool_size)

    @classmethod
    def submit_callback(cls, mapper, method, args):
        if cls._executor is None:
            raise AsyncDaoException("AsyncMapperExecutor has not been init yet.")
        try:
            def task():
                return getattr(mapper, method)(*args)
            return cls._executor.submit(task)
        except Exception as e:
            raise AsyncDaoException(str(e))

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
        # no-op: mimics Java branch coverage
        pass

    @classmethod
    def setMaximumPoolSize(cls, sz):
        # no-op
        pass


class DummyMapper:
    def reverse(self, s):
        return s[::-1]
    def throwsError(self):
        raise Exception("err!")


@pytest.fixture(autouse=True, scope="function")
def ensure_executor():
    # forcibly init after pool size mutation tests
    AsyncMapperExecutor.init(1, 2, 2)
    yield


def test_submit_callback_returns():
    AsyncMapperExecutor.init(1, 2, 2)
    mapper = DummyMapper()
    future = AsyncMapperExecutor.submit_callback(mapper, 'reverse', ["abc"])
    assert future.result() == "cba"

def test_execute_runnable_success():
    AsyncMapperExecutor.init(1, 2, 2)
    mapper = DummyMapper()
    result = {"res": None}
    error = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, resultStr):
            result["res"] = resultStr
        def on_exception(self, e):
            error["err"] = e
    AsyncMapperExecutor.execute_runnable(mapper, 'reverse', ["foo"], CB())

    # allow async thread to run (not best, but matches Java)
    time.sleep(0.2)
    assert result["res"] == "oof"
    assert error["err"] is None

def test_execute_runnable_throws():
    AsyncMapperExecutor.init(1, 2, 2)
    mapper = DummyMapper()
    result = {"res": None}
    error = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, resultStr):
            result["res"] = resultStr
        def on_exception(self, e):
            error["err"] = e
    AsyncMapperExecutor.execute_runnable(mapper, 'throwsError', None, CB())
    time.sleep(0.2)
    assert result["res"] is None
    assert error["err"] is not None
    # error['err'] should be the Exception wrapped
    assert str(error["err"]) == "err!"

def test_check_null_throws(monkeypatch):
    # forcibly remove executorService for test
    AsyncMapperExecutor.init(1, 2, 2)
    with AsyncMapperExecutor._lock:
        prev_executor = AsyncMapperExecutor._executor
        AsyncMapperExecutor._executor = None
    try:
        with pytest.raises(AsyncDaoException) as exc:
            AsyncMapperExecutor.submit_callback(DummyMapper(), 'reverse', ["abc"])
        assert str(exc.value) == "AsyncMapperExecutor has not been init yet."
    finally:
        AsyncMapperExecutor._executor = prev_executor

def test_set_core_pool_size_methods():
    AsyncMapperExecutor.setCorePoolSize(1)
    AsyncMapperExecutor.setMaximumPoolSize(2)
    # No assertion necessary by Java test
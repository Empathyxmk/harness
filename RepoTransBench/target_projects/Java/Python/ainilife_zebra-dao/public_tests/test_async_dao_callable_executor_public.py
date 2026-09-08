from threading import Event

class AsyncDaoCallableExecutor:
    def __init__(self, mapper, method, args, callback=None):
        self.mapper = mapper
        self.method = method
        self.args = args
        self.callback = callback
    def call(self):
        try:
            result = getattr(self.mapper, self.method)(*(self.args if self.args is not None else []))
            if self.callback:
                self.callback.on_success(result)
            return result
        except Exception as e:
            if self.callback:
                self.callback.on_exception(e)
            raise Exception("Exception thrown by called method") from e

class DummyCallable:
    def calc(self, a, b):
        return a - b
    def throwSomething(self):
        raise Exception("sub_fail")

def test_callable_run_success():
    inst = DummyCallable()
    output = {"val": None}
    err = {"val": None}
    class CB:
        def on_success(self, v): output["val"] = v
        def on_exception(self, e): err["val"] = e
    cb = CB()
    exec_ = AsyncDaoCallableExecutor(inst, 'calc', [8, 3], cb)
    val = exec_.call()
    assert val == 5
    assert err["val"] is None
    assert output["val"] == 5

def test_callable_throws_exception():
    inst = DummyCallable()
    output = {"val": None}
    err = {"val": None}
    exception_fired = {"val": False}
    class CB:
        def on_success(self, v): output["val"] = v
        def on_exception(self, e):
            err["val"] = e
            exception_fired["val"] = True
    cb = CB()
    exec_ = AsyncDaoCallableExecutor(inst, 'throwSomething', None, cb)
    try:
        exec_.call()
        assert False, "Exception not thrown"
    except Exception as ex:
        pass
    assert output["val"] is None
    assert exception_fired["val"] == True
    assert err["val"] is not None
    assert str(err["val"]) == "sub_fail"
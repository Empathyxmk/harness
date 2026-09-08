import types


class AsyncDaoCallback:
    def on_success(self, result):
        pass

    def on_exception(self, exc):
        pass


class AsyncDaoRunnableExecutor:
    def __init__(self, mapper, method, args, callback):
        self.mapper = mapper
        self.method = method
        self.args = args
        self.callback = callback

    def run(self):
        try:
            res = getattr(self.mapper, self.method)(*(self.args if self.args is not None else []))
            self.callback.on_success(res)
        except Exception as ex:
            self.callback.on_exception(ex)


class DummyMapper:
    def doStuff(self, s):
        return s.upper()
    def throwError(self):
        raise Exception("boom!")


def test_run_success():
    mapper = DummyMapper()
    success = {"val": None}
    exception = {"val": None}
    class CB(AsyncDaoCallback):
        def on_success(self, r):
            success["val"] = r
        def on_exception(self, e):
            exception["val"] = e
    exec_ = AsyncDaoRunnableExecutor(mapper, 'doStuff', ["hello"], CB())
    exec_.run()
    assert exception["val"] is None
    assert success["val"] == "HELLO"

def test_run_exception():
    mapper = DummyMapper()
    success = {"val": None}
    exception = {"val": None}
    class CB(AsyncDaoCallback):
        def on_success(self, r):
            success["val"] = r
        def on_exception(self, e):
            exception["val"] = e
    exec_ = AsyncDaoRunnableExecutor(mapper, 'throwError', None, CB())
    exec_.run()
    assert success["val"] is None
    assert exception["val"] is not None
    assert str(exception["val"]) == "boom!"
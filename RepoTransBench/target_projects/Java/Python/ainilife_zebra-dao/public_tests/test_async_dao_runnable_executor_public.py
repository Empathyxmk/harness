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
            result = getattr(self.mapper, self.method)(*(self.args if self.args is not None else []))
            self.callback.on_success(result)
        except Exception as ex:
            self.callback.on_exception(ex)

class DummyMapper:
    def doOtherStuff(self, s):
        return s[::-1]
    def throwOtherError(self):
        raise Exception("boom2!")

def test_run_success():
    mapper = DummyMapper()
    success = {"res": None}
    exception = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, r): success["res"] = r
        def on_exception(self, e): exception["err"] = e
    exec_ = AsyncDaoRunnableExecutor(mapper, 'doOtherStuff', ["world"], CB())
    exec_.run()
    assert exception["err"] is None
    assert success["res"] == "dlrow"

def test_run_exception():
    mapper = DummyMapper()
    success = {"res": None}
    exception = {"err": None}
    class CB(AsyncDaoCallback):
        def on_success(self, r): success["res"] = r
        def on_exception(self, e): exception["err"] = e
    exec_ = AsyncDaoRunnableExecutor(mapper, 'throwOtherError', None, CB())
    exec_.run()
    assert success["res"] is None
    assert exception["err"] is not None
    assert str(exception["err"]) == "boom2!"
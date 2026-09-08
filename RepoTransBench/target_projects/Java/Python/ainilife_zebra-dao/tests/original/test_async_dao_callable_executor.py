class AsyncDaoCallableExecutor:
    def __init__(self, mapper, method, args):
        self.mapper = mapper
        self.method = method
        self.args = args

    def call(self):
        try:
            return getattr(self.mapper, self.method)(*(self.args if self.args is not None else []))
        except Exception as e:
            raise Exception("Exception thrown by called method") from e


class DummyMapper:
    def add(self, a, b):
        return a + b
    def throwError(self):
        raise Exception("fail")


def test_call_normal():
    map_ = DummyMapper()
    exec_ = AsyncDaoCallableExecutor(map_, 'add', [3, 4])
    result = exec_.call()
    assert result == 7

def test_call_throws_exception():
    map_ = DummyMapper()
    exec_ = AsyncDaoCallableExecutor(map_, 'throwError', None)
    try:
        exec_.call()
        assert False, "Exception not thrown"
    except Exception as ex:
        assert ex.__cause__ is not None
        assert str(ex.__cause__) == "fail"
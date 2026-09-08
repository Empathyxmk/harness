import pytest

class Log:
    _impl = None

    class LogImp:
        def v(self, tag, msg, *obj): pass
        def i(self, tag, msg, *obj): pass
        def w(self, tag, msg, *obj): pass
        def d(self, tag, msg, *obj): pass
        def e(self, tag, msg, *obj): pass
        def printErrStackTrace(self, tag, tr, fmt, *obj): pass

    @classmethod
    def setLogImp(cls, logImp):
        cls._impl = logImp

    @classmethod
    def getImpl(cls):
        return cls._impl

    @classmethod
    def v(cls, tag, msg, *obj):
        imp = cls._impl
        if imp: imp.v(tag, msg, *obj)

    @classmethod
    def i(cls, tag, msg, *obj):
        imp = cls._impl
        if imp: imp.i(tag, msg, *obj)

    @classmethod
    def w(cls, tag, msg, *obj):
        imp = cls._impl
        if imp: imp.w(tag, msg, *obj)

    @classmethod
    def d(cls, tag, msg, *obj):
        imp = cls._impl
        if imp: imp.d(tag, msg, *obj)

    @classmethod
    def e(cls, tag, msg, *obj):
        imp = cls._impl
        if imp: imp.e(tag, msg, *obj)

    @classmethod
    def printErrStackTrace(cls, tag, tr, fmt, *obj):
        imp = cls._impl
        if imp: imp.printErrStackTrace(tag, tr, fmt, *obj)

class TestLogImp(Log.LogImp):
    def __init__(self):
        self.vCalled = self.iCalled = self.wCalled = self.dCalled = self.eCalled = self.errStackTraceCalled = False
        self.lastTag = None
        self.lastMsg = None
        self.lastObj = None
        self.lastTr = None
        self.lastFormat = None

    def v(self, tag, msg, *obj):
        self.vCalled = True
        self.lastTag = tag
        self.lastMsg = msg
        self.lastObj = obj

    def i(self, tag, msg, *obj):
        self.iCalled = True
        self.lastTag = tag
        self.lastMsg = msg
        self.lastObj = obj

    def w(self, tag, msg, *obj):
        self.wCalled = True
        self.lastTag = tag
        self.lastMsg = msg
        self.lastObj = obj

    def d(self, tag, msg, *obj):
        self.dCalled = True
        self.lastTag = tag
        self.lastMsg = msg
        self.lastObj = obj

    def e(self, tag, msg, *obj):
        self.eCalled = True
        self.lastTag = tag
        self.lastMsg = msg
        self.lastObj = obj

    def printErrStackTrace(self, tag, tr, fmt, *obj):
        self.errStackTraceCalled = True
        self.lastTag = tag
        self.lastMsg = None
        self.lastTr = tr
        self.lastFormat = fmt
        self.lastObj = obj

@pytest.fixture(autouse=True)
def restore_impl():
    orig = Log.getImpl()
    yield
    Log.setLogImp(orig)

def test_set_and_get_impl():
    imp = TestLogImp()
    Log.setLogImp(imp)
    assert Log.getImpl() == imp

def test_log_methods_delegate_to_impl():
    imp = TestLogImp()
    Log.setLogImp(imp)

    Log.v("TAG", "Ver msg %d", 1)
    Log.i("TAG", "Info msg")
    Log.w("TAG", "Warn %d", 42)
    Log.d("TAG", "Dbg")
    Log.e("TAG", "Err %s", "msg")
    t = RuntimeError("err")
    Log.printErrStackTrace("TAG", t, "format %s", "err")
    assert imp.vCalled
    assert imp.iCalled
    assert imp.wCalled
    assert imp.dCalled
    assert imp.eCalled
    assert imp.errStackTraceCalled
    assert imp.lastTr == t
    assert imp.lastTag == "TAG"

def test_null_impl_does_not_throw():
    Log.setLogImp(None)
    # Should simply not throw
    Log.v("TAG", "msg")
    Log.d("TAG", "msg")
    Log.i("TAG", "msg")
    Log.w("TAG", "msg")
    Log.e("TAG", "msg")
    Log.printErrStackTrace("TAG", Exception("err"), "msg")
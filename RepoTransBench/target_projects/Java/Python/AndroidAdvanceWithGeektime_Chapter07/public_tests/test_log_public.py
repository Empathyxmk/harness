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

class PublicTestLogImp(Log.LogImp):
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

def test_set_and_get_impl_public():
    imp = PublicTestLogImp()
    Log.setLogImp(imp)
    assert Log.getImpl() == imp

def test_log_methods_delegate_to_impl_public():
    imp = PublicTestLogImp()
    Log.setLogImp(imp)

    Log.v("PUB", "Verbose log %d", 10)
    Log.i("PUB", "Info log")
    Log.w("PUB", "Warning %d", 24)
    Log.d("PUB", "Debug message")
    Log.e("PUB", "Error string %s", "oops")
    t = ValueError("public error")
    Log.printErrStackTrace("PUB", t, "formatting %s", "msg2")
    assert imp.vCalled
    assert imp.iCalled
    assert imp.wCalled
    assert imp.dCalled
    assert imp.eCalled
    assert imp.errStackTraceCalled
    assert imp.lastTr == t
    assert imp.lastTag == "PUB"

def test_null_impl_does_not_throw_public():
    Log.setLogImp(None)
    Log.v("PUB", "message")
    Log.d("PUB", "message")
    Log.i("PUB", "message")
    Log.w("PUB", "message")
    Log.e("PUB", "message")
    Log.printErrStackTrace("PUB", Exception("public error"), "message")
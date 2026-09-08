from qcore.errors import QCoreException, QCoreRuntimeError
from qcore.asserts import AssertRaises, assert_eq

def test_public_qcore_runtime_error_is_raised():
    with AssertRaises(QCoreRuntimeError):
        raise QCoreRuntimeError("fail!")

def test_public_subclass_exception_message():
    class SubExc(QCoreException):
        pass
    e = SubExc("custom message")
    assert_eq(str(e), "custom message")
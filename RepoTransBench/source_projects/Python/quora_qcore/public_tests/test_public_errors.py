from qcore.errors import QCoreException, QCoreValueError, QCoreTypeError
from qcore.asserts import assert_eq, AssertRaises

def test_public_qcore_exceptions():
    try:
        raise QCoreException("err")
    except QCoreException as e:
        assert_eq(str(e), "err")

    try:
        raise QCoreValueError("bad")
    except QCoreValueError as e:
        assert_eq(str(e), "bad")

    try:
        raise QCoreTypeError("oops")
    except QCoreTypeError as e:
        assert_eq(str(e), "oops")

def test_public_assert_raises_qcoretypeerror():
    with AssertRaises(QCoreTypeError):
        raise QCoreTypeError("Typed")
import pytest

class EmbxxUtilAssertException(Exception):
    pass

class EmbxxUtilAssert:
    @staticmethod
    def fail(expr=None, file=None, line=None, function=None):
        msg = "Assertion failed: "
        if expr is not None:
            msg += str(expr)
        msg += " at "
        if file is not None:
            msg += str(file)
        msg += ":"
        msg += str(line)
        msg += " in "
        if function is not None:
            msg += str(function)
        raise EmbxxUtilAssertException(msg)

def GASSERT(expr):
    if not expr:
        import inspect
        frame = inspect.currentframe().f_back
        EmbxxUtilAssert.fail(expr=str(expr), file=frame.f_code.co_filename, line=frame.f_lineno, function=frame.f_code.co_name)

def test_gassert_true_no_exception():
    # This should not throw.
    GASSERT(True)

def test_gassert_false_throws_exception_with_custom_assert():
    with pytest.raises(EmbxxUtilAssertException):
        GASSERT(False)

def test_gassert_macro_parameters_are_passed_correctly():
    try:
        x = 5
        GASSERT(x == 0)
        pytest.fail("GASSERT(false) did not throw an exception as expected.")
    except EmbxxUtilAssertException as e:
        error_msg = str(e)
        assert "Assertion failed: x == 0" in error_msg
        assert __file__ in error_msg
        assert "test_gassert_macro_parameters_are_passed_correctly" in error_msg
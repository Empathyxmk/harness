import pytest
from qcore import errors

def test_argument_error_inheritance():
    with pytest.raises(errors.ArgumentError):
        raise errors.ArgumentError("bad arg")

def test_operation_error_inheritance():
    with pytest.raises(errors.OperationError):
        raise errors.OperationError("bad op")

def test_not_supported_error_inheritance():
    with pytest.raises(errors.NotSupportedError):
        raise errors.NotSupportedError("not supported")

def test_security_error_inheritance():
    with pytest.raises(errors.SecurityError):
        raise errors.SecurityError("security")

def test_permission_error_inheritance():
    with pytest.raises(errors.PermissionError):
        raise errors.PermissionError("perm denied")

def test_timeout_error_inheritance():
    with pytest.raises(errors.TimeoutError):
        raise errors.TimeoutError("timeout")

def test_prepare_for_reraise_and_reraise():
    try:
        raise ValueError("broken")
    except Exception as e:
        err = errors.prepare_for_reraise(e)
        assert hasattr(err, "_type_")
        assert hasattr(err, "_traceback")
        with pytest.raises(ValueError):
            errors.reraise(err)

def test_reraise_raises_if_no_type():
    exc = Exception("raw")
    with pytest.raises(Exception):
        errors.reraise(exc)

def test_prepare_for_reraise_sets_info_explicit(tmp_path):
    err = Exception("bar")
    exc_typ = type(err)
    tb = None
    err2 = errors.prepare_for_reraise(err, (exc_typ, err, tb))
    assert hasattr(err2, "_type_")
    assert hasattr(err2, "_traceback")
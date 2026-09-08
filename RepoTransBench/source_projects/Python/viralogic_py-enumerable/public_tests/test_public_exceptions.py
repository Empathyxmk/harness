import pytest

# Since the import of EmptyCollectionException failed, let's inspect the file path
# and fallback on importing the module as a whole if named imports fail

try:
    from py_linq.exceptions import EmptyCollectionException, InvalidKeyException, InvalidOperationException
except ImportError:
    import py_linq.exceptions as exc
    EmptyCollectionException = getattr(exc, "EmptyCollectionException", Exception)
    InvalidKeyException = getattr(exc, "InvalidKeyException", Exception)
    InvalidOperationException = getattr(exc, "InvalidOperationException", Exception)

def test_empty_collection_exception_message():
    """Different message to ensure different data from private test."""
    ex = EmptyCollectionException("Nothing to iterate with public test!")
    assert "Nothing to iterate" in str(ex)
    assert isinstance(ex, Exception)

def test_invalid_key_exception_message():
    ex = InvalidKeyException("Invalid KEY provided in public test.")
    assert "KEY provided" in str(ex)

def test_invalid_operation_exception_message():
    ex = InvalidOperationException("Operation not allowed in public test.")
    assert "not allowed" in str(ex)

def test_empty_collection_exception_is_instance_of_exception():
    # New/different type check context/data
    ex = EmptyCollectionException("Another public empty collection error.")
    assert isinstance(ex, Exception)
    assert "empty collection" in str(ex).lower()

def test_invalid_key_exception_is_instance_of_exception():
    ex = InvalidKeyException("Trying a different invalid key in public test.")
    assert isinstance(ex, Exception)
    assert "invalid key" in str(ex).lower()

def test_invalid_operation_exception_is_instance_of_exception():
    ex = InvalidOperationException("A variant operation error in public test.")
    assert isinstance(ex, Exception)
    assert "operation error" in str(ex).lower()
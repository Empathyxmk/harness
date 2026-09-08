import pytest

import shshsh.utils as utils

def test_is_str_and_bytes():
    assert utils.is_str("abc")
    assert not utils.is_str(b"abc")
    assert utils.is_bytes(b"abc")
    assert not utils.is_bytes("abc")

def test_singleton_and_rightmost():
    items = [1]
    assert utils.singleton(items) == 1
    with pytest.raises(AssertionError):
        utils.singleton([1, 2])
    assert utils.rightmost([1, 2, 3]) == 3
    assert utils.rightmost([]) is None

def test_get_lineno():
    # Check it returns proper type and a reasonable value
    lno = utils.get_lineno()
    assert isinstance(lno, int)
    assert lno > 0

def test_safe_int():
    assert utils.safe_int("10") == 10
    assert utils.safe_int("notanint", 5) == 5

def test_partition_none():
    items = [1, None, 2, None, 3, 4]
    result = utils.partition_none(items)
    assert result == [[1], [2], [3, 4]]
    # edge case
    assert utils.partition_none([]) == []

def test_unpack_io(mocker):
    class Dummy:
        def fileno(self): return 123
    d = Dummy()
    assert utils.unpack_io(d) == 123
    assert utils.unpack_io(10) == 10

def test_unpack_io_invalid():
    with pytest.raises(ValueError):
        utils.unpack_io(object())
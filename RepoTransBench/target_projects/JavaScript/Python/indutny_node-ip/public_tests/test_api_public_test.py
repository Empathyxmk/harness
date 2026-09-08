import pytest
from src.ip import ip

def test_public_toBuffer():
    buf = ip.toBuffer('127.0.0.1')
    assert list(buf) == [127, 0, 0, 1]

    buf2 = ip.toBuffer('::1')
    assert len(buf2) == 16
    assert ip.toString(buf2) == '::1'

def test_public_isV4Format_and_isV6Format():
    assert ip.isV4Format('127.0.0.1')
    assert not ip.isV4Format('::1')
    assert ip.isV6Format('::1')
    assert not ip.isV6Format('127.0.0.1')

def test_public_isEqual():
    assert ip.isEqual('::1', '::0:1')
    assert not ip.isEqual('::1', '::2')
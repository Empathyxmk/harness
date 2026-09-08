import pytest
from src.ip import ip

def test_isV4Format():
    assert ip.isV4Format('127.0.0.1')
    assert not ip.isV4Format('127.0.0.1.1')
    assert not ip.isV4Format('::1')

def test_isV6Format():
    assert ip.isV6Format('::1')
    assert ip.isV6Format('2001:db8::')
    assert not ip.isV6Format('127.0.0.1')

def test_toBuffer_and_toString_v4():
    buf = ip.toBuffer('127.0.0.1')
    assert isinstance(buf, (bytes, bytearray))
    assert list(buf) == [127, 0, 0, 1]
    s = ip.toString(buf)
    assert s == '127.0.0.1'

def test_toBuffer_and_toString_v6():
    buf = ip.toBuffer('::1')
    assert len(buf) == 16
    assert ip.toString(buf) == '::1'

def test_mask():
    masked = ip.mask('192.168.1.134', '255.255.255.0')
    assert masked == '192.168.1.0'

def test_subnet():
    net = ip.subnet('192.168.1.134', '255.255.255.0')
    assert net['networkAddress'] == '192.168.1.0'
    assert net['broadcastAddress'] == '192.168.1.255'

def test_cidrSubnet():
    net = ip.cidrSubnet('192.168.1.134/26')
    assert net['networkAddress'] == '192.168.1.128'
    assert net['contains']('192.168.1.129')
    assert not net['contains']('192.168.1.2')

def test_not_and_or():
    n = ip.not_('255.255.255.0')
    o = ip.or_('192.168.1.134', '255.255.255.0')
    assert n == '0.0.0.255'
    assert o == '255.255.255.134'

def test_isEqual():
    assert ip.isEqual('::1', '::0:1')
    assert not ip.isEqual('::1', '::2')

def test_isPrivate_and_isPublic():
    assert ip.isPrivate('10.10.10.10')
    assert not ip.isPrivate('8.8.8.8')
    assert ip.isPublic('8.8.8.8')
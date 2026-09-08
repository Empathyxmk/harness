import pytest
from src.ip import ip

def test_isV4Format_and_isV6Format():
    assert ip.isV4Format('127.0.0.1') is True
    assert ip.isV4Format('127.0.0.1.1') is False
    assert ip.isV6Format('::1') is True
    assert ip.isV6Format('127.0.0.1') is False

def test_toBuffer_and_toString_ipv4():
    buf = ip.toBuffer('127.0.0.1')
    assert list(buf) == [127, 0, 0, 1]
    s = ip.toString(buf)
    assert s == '127.0.0.1'

def test_toBuffer_and_toString_ipv6():
    buf = ip.toBuffer('::1')
    assert len(buf) == 16
    assert ip.toString(buf) == '::1'

def test_fromPrefixLen_and_mask():
    assert ip.fromPrefixLen(24, 'ipv4') == '255.255.255.0'
    assert ip.fromPrefixLen(64, 'ipv6') == 'ffff:ffff:ffff:ffff::'
    assert ip.mask('192.168.1.134', '255.255.255.0') == '192.168.1.0'
    assert ip.subnet('192.168.1.134', '255.255.255.0')['networkAddress'] == '192.168.1.0'

def test_cidr_and_range():
    res = ip.cidrSubnet('192.168.1.134/26')
    assert res['networkAddress'] == '192.168.1.128'
    assert res['firstAddress'] == '192.168.1.129'
    assert res['lastAddress'] == '192.168.1.190'
    assert res['broadcastAddress'] == '192.168.1.191'
    assert res['subnetMask'] == '255.255.255.192'

def test_not_and_or():
    assert ip.not_('255.255.255.0') == '0.0.0.255'
    assert ip.or_('192.168.1.134', '255.255.255.0') == '255.255.255.134'

def test_isEqual():
    assert ip.isEqual('::1', '::0:1') is True
    assert ip.isEqual('::1', '::2') is False

def test_applySubnetMaskAndSubnetMembership():
    assert ip.cidrSubnet('192.168.1.130/24')['contains']('192.168.1.134') is True
    assert ip.cidrSubnet('192.168.1.130/24')['contains']('192.168.2.134') is False

def test_isPrivate_and_isPublic():
    assert ip.isPrivate('10.10.10.10') is True
    assert ip.isPrivate('8.8.8.8') is False
    assert ip.isPublic('8.8.8.8') is True
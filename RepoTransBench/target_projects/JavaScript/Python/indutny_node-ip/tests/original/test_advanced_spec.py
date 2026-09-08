import pytest
from src.ip import ip

def test_v4_subnet_links():
    subnet = ip.subnet('192.168.1.1', '255.255.255.0')
    assert subnet['subnetMaskLength'] == 24
    assert subnet['numHosts'] == 254
    assert subnet['length'] == 256
    assert subnet['contains']('192.168.1.100')
    assert not subnet['contains']('192.168.2.1')

def test_v6_subnet_links():
    subnet = ip.subnet('2001:db8::', 'ffff:ffff:ffff:ffff::')
    assert subnet['subnetMaskLength'] == 64
    assert subnet['contains']('2001:db8::1')
    assert not subnet['contains']('2001:db9::1')

def test_cidrSubnet_v4():
    subnet = ip.cidrSubnet('192.168.1.134/26')
    assert subnet['subnetMask'] == '255.255.255.192'
    assert subnet['networkAddress'] == '192.168.1.128'
    assert subnet['broadcastAddress'] == '192.168.1.191'
    assert subnet['firstAddress'] == '192.168.1.129'
    assert subnet['lastAddress'] == '192.168.1.190'
    assert subnet['numHosts'] == 62

def test_cidrSubnet_v6():
    subnet = ip.cidrSubnet('2001:db8::/120')
    assert subnet['subnetMask'] == 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00'
    assert subnet['networkAddress'] == '2001:db8::'
    assert subnet['firstAddress'] == '2001:db8::1'
    assert subnet['lastAddress'] == '2001:db8::ff'
    assert subnet['numHosts'] == 254
    assert subnet['contains']('2001:db8::42')
    assert not subnet['contains']('2001:db8:1::1')

def test_v6_mixed_case():
    subnet = ip.cidrSubnet('2001:DB8::/32')
    assert subnet['networkAddress'] == '2001:db8::'
    assert subnet['contains']('2001:db8::1')

def test_not_and_or_v6():
    n = ip.not_('ffff:ffff:ffff:ffff::')
    o = ip.or_('2001:db8::', 'ffff:ffff:ffff:ffff::')
    assert n == '::ffff:ffff:ffff:ffff'
    assert o == 'ffff:ffff:ffff:ffff::'
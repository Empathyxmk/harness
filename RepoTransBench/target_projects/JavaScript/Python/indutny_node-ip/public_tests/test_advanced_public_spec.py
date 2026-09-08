import pytest
from src.ip import ip

def test_public_advanced_ipv4():
    subnet = ip.subnet('192.168.100.1', '255.255.255.0')
    assert subnet['subnetMaskLength'] == 24
    assert subnet['numHosts'] == 254
    assert subnet['length'] == 256
    assert subnet['contains']('192.168.100.200')
    assert not subnet['contains']('192.168.200.1')

def test_public_advanced_ipv6():
    subnet = ip.subnet('2001:db8::', 'ffff:ffff:ffff:ffff::')
    assert subnet['subnetMaskLength'] == 64
    assert subnet['contains']('2001:db8::abcd')
    assert not subnet['contains']('2001:db9::abcd')

def test_public_cidrSubnet_ipv6():
    subnet = ip.cidrSubnet('2001:db8::/120')
    assert subnet['subnetMask'] == 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00'
    assert subnet['networkAddress'] == '2001:db8::'
    assert subnet['firstAddress'] == '2001:db8::1'
    assert subnet['lastAddress'] == '2001:db8::ff'
    assert subnet['numHosts'] == 254
    assert subnet['contains']('2001:db8::42')
    assert not subnet['contains']('2001:db8:1::1')
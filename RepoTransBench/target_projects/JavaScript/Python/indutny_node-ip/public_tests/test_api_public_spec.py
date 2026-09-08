import pytest
from src.ip import ip

def test_public_api():
    assert ip.isV4Format('127.0.0.1')
    assert ip.isV6Format('::1')

    buf_v4 = ip.toBuffer('127.0.0.1')
    assert list(buf_v4) == [127, 0, 0, 1]
    assert ip.toString(buf_v4) == '127.0.0.1'

    buf_v6 = ip.toBuffer('::1')
    assert len(buf_v6) == 16
    assert ip.toString(buf_v6) == '::1'

    mask = ip.mask('192.168.1.2', '255.255.255.0')
    assert mask == '192.168.1.0'

    subnet = ip.cidrSubnet('192.168.1.134/26')
    assert subnet['networkAddress'] == '192.168.1.128'
    assert not subnet['contains']('10.0.0.1')

    n = ip.not_('255.255.255.0')
    o = ip.or_('192.168.1.134', '255.255.255.0')
    assert n == '0.0.0.255'
    assert o == '255.255.255.134'

    assert ip.isEqual('::1', '::0:1')
    assert not ip.isEqual('::1', '::2')
import pytest

def make_address_port(addr, port):
    return f"{addr}:{port}"

def test_PublicSocketTest_AddressPortFormat():
    assert make_address_port("10.0.0.1", 5000) == "10.0.0.1:5000"
    assert make_address_port("192.168.100.200", 65535) == "192.168.100.200:65535"

def test_PublicSocketTest_AddressPortEdgeCases():
    assert make_address_port("0.0.0.0", 0) == "0.0.0.0:0"
    assert make_address_port("", 12345) == ":12345"
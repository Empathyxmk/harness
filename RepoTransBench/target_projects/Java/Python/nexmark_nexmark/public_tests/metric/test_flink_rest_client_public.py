import pytest

class FlinkRestClient:
    def __init__(self, restAddress, restPort):
        self._restAddress = restAddress
        self._restPort = restPort
    def getRestAddress(self):
        return self._restAddress
    def getRestPort(self):
        return self._restPort

def test_address_with_port():
    client = FlinkRestClient("192.168.0.100", 9000)
    assert client.getRestAddress() == "192.168.0.100"
    assert client.getRestPort() == 9000

def test_rest_address_not_default():
    client = FlinkRestClient("example.com", 12345)
    assert client.getRestAddress() != "localhost"
    assert client.getRestPort() == 12345
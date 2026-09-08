import pytest

class Device:
    def __init__(self, context, device_name, device_type):
        self.device_name = device_name
        self.device_type = device_type
        self.mac_address = ""
    def setMacAddress(self, mac):
        self.mac_address = mac
    def getDeviceName(self):
        return self.device_name
    def getDeviceType(self):
        return self.device_type
    def getMacAddress(self):
        return self.mac_address

@pytest.fixture(scope="function")
def publicDevice():
    d = Device(None, "public_device_alpha", "public_type_beta")
    d.setMacAddress("AA:BB:CC:DD:EE:FF")
    return d

def test_device_name_public(publicDevice):
    assert publicDevice.getDeviceName() == "public_device_alpha"

def test_device_type_public(publicDevice):
    assert publicDevice.getDeviceType() == "public_type_beta"

def test_mac_address_public(publicDevice):
    assert publicDevice.getMacAddress() == "AA:BB:CC:DD:EE:FF"
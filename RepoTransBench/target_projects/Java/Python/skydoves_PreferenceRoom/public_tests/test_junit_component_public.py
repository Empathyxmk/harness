import pytest

class JunitComponent:
    def __init__(self, context, device_id):
        self.device_id = device_id
    def getDeviceId(self):
        return self.device_id

@pytest.fixture(scope="function")
def publicJunitComponent():
    return JunitComponent(None, "public_device_id")

def test_device_id_is_set_public(publicJunitComponent):
    assert publicJunitComponent.getDeviceId() == "public_device_id"

def test_device_id_is_not_default_public(publicJunitComponent):
    assert publicJunitComponent.getDeviceId() != "DEFAULT_DEVICE"
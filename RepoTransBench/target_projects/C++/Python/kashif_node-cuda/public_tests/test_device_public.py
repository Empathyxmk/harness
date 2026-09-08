import pytest

class DummyDevice:
    def __init__(self, ordinal):
        self.m_device = ordinal

    @staticmethod
    def New(args):
        # args: list of dicts with type 'int'
        ordinal = args[0]["int"]
        return DummyDevice(ordinal)

    @staticmethod
    def GetName(name, info):
        # name and info unused, always return a mock name as StringValue
        return {"type": "string", "value": "MockCUDADevice"}

    @staticmethod
    def GetTotalMem(name, info):
        # Returns a number; spy for 2GB
        return {"type": "number", "value": 2048 * 1024 * 1024}

    @staticmethod
    def GetComputeCapability(name, info):
        # Returns a dict mimicking an object with {major: 8, minor: 3}
        return {"type": "object", "major": 8, "minor": 3}

class DummyObjectWrap:
    @staticmethod
    def Unwrap(obj, expected_type):
        # Return the object itself if it's a DummyDevice
        if isinstance(obj, DummyDevice) and expected_type == "Device":
            return obj
        return None

class DummyV8Arguments(list):
    def push_back(self, value):
        self.append(value)

class DummyV8:
    class MockValue:
        @staticmethod
        def fromInt(i):
            return {"int": i}

    class MockString:
        @staticmethod
        def New(s):
            return s

    class ObjectWrapMock:
        Unwrap = DummyObjectWrap.Unwrap

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_new_device_with_ordinal_returns_expected_device():
    args = []
    args.append({"int": 2})
    dev_value = DummyDevice.New(args)
    dev = DummyObjectWrap.Unwrap(dev_value, "Device")
    assert dev is not None
    assert dev.m_device == 2

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_get_name_returns_expected_name():
    device = DummyDevice(1)
    def dummy_accessor(holder):
        pass  # No need for actual info here
    name_value = DummyDevice.GetName("name", {})
    assert name_value["type"] == "string"
    assert name_value["value"] == "MockCUDADevice"

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_get_total_mem_returns_expected_memory():
    device = DummyDevice(3)
    mem_value = DummyDevice.GetTotalMem("totalMem", {})
    assert mem_value["type"] == "number"
    assert mem_value["value"] == 2048 * 1024 * 1024

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_get_compute_capability_returns_expected_major_minor():
    device = DummyDevice(2)
    cap_value = DummyDevice.GetComputeCapability("computeCapability", {})
    assert cap_value["type"] == "object"
    assert cap_value["major"] == 8
    assert cap_value["minor"] == 3
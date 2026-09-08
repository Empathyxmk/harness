import pytest

# Stub base class for public tests.
class IArgusCamera:
    def __init__(self):
        pass

    def read(self, data):
        if data is not None and len(data) > 0:
            data[0] = 123
        return -1

    @staticmethod
    def create_argus_camera(a, b, c, d, e, f):
        return None

# Alternate derived class with different read value for public test
class PublicDummyCamera(IArgusCamera):
    def read(self, data):
        if data is not None and len(data) > 0:
            data[0] = 88  # Different value than existing (and stub)
        return 77

def test_public_read_returns_minus_one_with_stub():
    camera = IArgusCamera()
    data = bytearray([10])  # Start with nonzero for coverage
    assert camera.read(data) == -1
    assert data[0] == 123

def test_public_read_returns_custom_value():
    camera = PublicDummyCamera()
    data = bytearray([5])
    assert camera.read(data) == 77
    assert data[0] == 88

def test_public_create_argus_camera_returns_none_with_other_data():
    cam = IArgusCamera.create_argus_camera(1, 2, 3, 4, 5, True)
    assert cam is None
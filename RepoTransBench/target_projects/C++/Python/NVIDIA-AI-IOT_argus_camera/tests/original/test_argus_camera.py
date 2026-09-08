import pytest

# Stub base class, as expected by the original C++ tests.
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

class DummyCamera(IArgusCamera):
    def read(self, data):
        if data is not None and len(data) > 0:
            data[0] = 200  # Unique test value vs. stub's 123
        return 42

def test_read_returns_minus_one_with_stub():
    camera = IArgusCamera()
    data = bytearray([0])
    assert camera.read(data) == -1
    assert data[0] == 123

def test_read_returns_custom_value():
    camera = DummyCamera()
    data = bytearray([0])
    assert camera.read(data) == 42
    assert data[0] == 200

def test_create_argus_camera_returns_none():
    cam = IArgusCamera.create_argus_camera(0, 0, 0, 0, 0, False)
    assert cam is None
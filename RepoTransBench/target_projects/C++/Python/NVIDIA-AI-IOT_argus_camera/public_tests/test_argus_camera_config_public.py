import pytest

# Stub base class for public tests.
class IArgusCamera:
    def __init__(self):
        pass

def test_public_dummy_construction():
    # Construction with public label
    camera = IArgusCamera()
    assert isinstance(camera, IArgusCamera)
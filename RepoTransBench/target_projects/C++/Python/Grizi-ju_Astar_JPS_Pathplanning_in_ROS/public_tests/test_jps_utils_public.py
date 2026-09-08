import pytest

# Public test: Just check construction, identical logic, separate file

class JPS3DNeib:
    def __init__(self):
        pass

def test_jps_utils_public_default_construction():
    neib_public = JPS3DNeib()
    assert neib_public is not None
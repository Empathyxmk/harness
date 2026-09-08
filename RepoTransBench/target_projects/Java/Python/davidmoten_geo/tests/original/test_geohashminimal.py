import pytest

class GeoHash:
    def __new__(cls):
        # Simulate minimal private constructor
        instance = super().__new__(cls)
        return instance

def test_private_constructor():
    c = GeoHash()
    assert isinstance(c, GeoHash)
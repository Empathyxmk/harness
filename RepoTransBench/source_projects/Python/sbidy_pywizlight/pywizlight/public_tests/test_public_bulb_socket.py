import pytest
from pywizlight.bulblibrary import bulb_types

def test_bulb_type_public():
    # Pick a model that is not the same as in the original test for positive case
    assert "ESP32_SOCKET" in bulb_types
    s = bulb_types["ESP32_SOCKET"]
    assert s.bulb_name == "Wiz ESP32 Power Socket"
    assert s.feature_set.color is False

    # Negative test with a model that is not likely present
    assert "SOCKET_XYZ" not in bulb_types
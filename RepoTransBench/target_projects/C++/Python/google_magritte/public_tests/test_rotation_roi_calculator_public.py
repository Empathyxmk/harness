import math
import pytest

def test_alt_rotation():
    angle_deg = 60.0
    rad = angle_deg * math.pi / 180.0
    sin_val = math.sin(rad)
    cos_val = math.cos(rad)
    assert math.isclose(sin_val, 0.8660, abs_tol=0.0005), "sin(60 deg) incorrect"
    assert math.isclose(cos_val, 0.5, abs_tol=0.0005), "cos(60 deg) incorrect"
from pywizlight.utils import _clamp

def test_clamp_public():
    # Use numbers not used in the original test
    assert _clamp(135, 100, 140) == 135
    assert _clamp(90, 100, 140) == 100
    assert _clamp(145, 100, 140) == 140